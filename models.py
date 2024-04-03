from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Session(Base):
    __tablename__ = 'sessions'
    
    id = Column(String(36), primary_key=True, unique=True, nullable=False)
    original_file_path = Column(String(120), nullable=False)
    augmented_file_path = Column(String(120), nullable=True)

    def __repr__(self):
        return f'<Session {self.id}>'
    
class CopilotCapture(Base):
    __tablename__ = 'copilot_capture'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(36), nullable=False)
    request_method = Column(String(10))
    request_url = Column(String(255))
    request_body = Column(Text)
    response_status_code = Column(Integer)
    response_headers = Column(Text)
    response_body = Column(Text)
    parsed_content = Column(Text)

    def __repr__(self):
        return f'<CopilotCapture {self.id}>'
