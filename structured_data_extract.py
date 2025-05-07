from openai import OpenAI
from pydantic import BaseModel
import os
import json
client = OpenAI()

class ResearchPaperExtraction(BaseModel):
    title: str
    authors: list[str]
    abstract: str
    keywords: list[str]


papers_folder = "/Users/annhoward/Downloads/Papers"

for paper in os.listdir(papers_folder):
    paper_pdf = client.files.create(
        file=open(os.path.join(papers_folder, paper), "rb"),
        purpose="user_data"
    )
    
    try:
        response = client.responses.parse(
            model="gpt-4o-2024-08-06",
            input=[
                {
                    "role": "system",
                    "content": "You are an expert at structured data extraction. You will be given unstructured text from a research paper and should convert it into the given structure.",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_file",
                            "file_id": paper_pdf.id,
                        },
                        {
                            "type": "input_text",
                            "text": "Please extract the structured data from the paper. ",
                        },
                    ]
                }
            ],
            text_format=ResearchPaperExtraction,
        )

        research_paper = response.output_parsed
        
        ## append to research_papers.jsonl
        with open("./research_papers.jsonl", "a") as f:
            f.write(json.dumps(research_paper.model_dump()) + "\n")
    except Exception as e:
        print(f"Error processing {paper}: {e}")
        continue
