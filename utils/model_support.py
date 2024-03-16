def skill_finder(model,text):
  try:
    doc=model(text)
    doc=doc.ents
    skills=[]
    for ent in doc:
      label=ent.label_
      if label == "Skills":
        skills.append(ent.text)
    return list(set(skills))
  except Exception as error:
    return error
