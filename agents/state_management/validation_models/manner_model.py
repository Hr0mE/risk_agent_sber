from pydantic import BaseModel

class MannerInfo(BaseModel):
  """Данные о манере"""
  tone: str
  emotionality: str
  appeal: str
  additionally: list[str]

  def __repr__(self):
    print(f"MannerInfo(\n\tтон: {self.tone}\n\tэмоциональность: {self.emotionality}\n\tобращение: {self.appeal}\n\tдоп. информация: {self.additionally}\n)")
  
  def __str__(self):
    return f"MannerInfo(\n\tтон: {self.tone}\n\tэмоциональность: {self.emotionality}\n\tобращение: {self.appeal}\n\tдоп. информация: {self.additionally}\n)"
