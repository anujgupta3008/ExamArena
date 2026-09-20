import json
import boto3
import os
from .database import SessionLocal
from .models import Paper
from .pdf_parser import PDFParser
from .ai_tagger import AITagger
from pathlib import Path

def handler(event, context):
    """
    SQS handler for processing PDFs asynchronously.
    """
    s3 = boto3.client('s3')
    bucket = os.getenv("S3_BUCKET_NAME", "exam-arena-assets-ag")
    
    for record in event.get('Records', []):
        try:
            body = json.loads(record['body'])
            paper_id = body.get('paper_id')
            s3_key = body.get('s3_key')
            
            if not paper_id or not s3_key:
                print("Missing paper_id or s3_key in message")
                continue
                
            db = SessionLocal()
            try:
                paper = db.query(Paper).filter_by(id=paper_id).first()
                if not paper:
                    print(f"Paper {paper_id} not found")
                    continue
                
                # Download PDF from S3 to /tmp
                local_pdf_path = f"/tmp/{paper_id}.pdf"
                print(f"Downloading {s3_key} from bucket {bucket}")
                s3.download_file(bucket, s3_key, local_pdf_path)
                
                # Update paper with local pdf path (needed by parser for now)
                paper.pdf_path = local_pdf_path
                db.commit()
                
                parser = PDFParser()
                tagger = AITagger()
                
                print(f"Parsing PDF {local_pdf_path}...")
                slices = parser.parse_pdf(local_pdf_path, paper.id)
                
                staged_questions = []
                for slice_info in slices:
                    print(f"Tagging slice {slice_info['image_path']}")
                    tagged_metadata = tagger.tag_question_image(slice_info["image_path"])
                    tagged_metadata["image_path"] = slice_info["image_path"]
                    staged_questions.append(tagged_metadata)
                
                # Save staged to S3
                staged_s3_key = f"staged/{paper.id}.json"
                print(f"Uploading staged data to {staged_s3_key}")
                s3.put_object(
                    Bucket=bucket,
                    Key=staged_s3_key,
                    Body=json.dumps(staged_questions, indent=2).encode('utf-8'),
                    ContentType="application/json"
                )
                
                # Cleanup local PDF
                if os.path.exists(local_pdf_path):
                    os.remove(local_pdf_path)
                    
                print(f"Successfully processed paper {paper_id}")
            finally:
                db.close()
        except Exception as e:
            print(f"Error processing record: {e}")
            raise e
            
    return {"statusCode": 200, "body": json.dumps({"message": "Processed successfully"})}
