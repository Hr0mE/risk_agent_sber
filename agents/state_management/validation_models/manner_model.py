from pydantic import BaseModel


class MannerInfo(BaseModel):
  """Данные о манере"""
  tone: str
  emotionality: str
  appeal: str
  additionally: list[str]

  def __repr__(self):
    return f"MannerInfo( \
      \n\ttone: {self.tone} \
      \n\temotionality: {self.emotionality} \
      \n\tappeal: {self.appeal} \
      \n\tadditionally: {self.additionally} \
    \n)"
  
  def __str__(self):
    return f"Данные о манере: \
      \n\tтон: {self.tone} \
      \n\tэмоциональность: {self.emotionality} \
      \n\tобращение: {self.appeal} \
      \n\tдоп. информация: {self.additionally} \
    \n)"