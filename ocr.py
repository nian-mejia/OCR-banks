import os
import re
import cv2 
import pytesseract

from date_utils import parse_date

def get_image_path():
    desktop_path = "/Users/nmejia/Desktop"
    files = os.listdir(desktop_path)
    files = [file for file in files if file[0] != "."]
    files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(desktop_path, x)), reverse=True)
    return desktop_path + "/" + files[0]

def main(type):
  image_path = get_image_path()

  img = cv2.imread(image_path)

  # Adding custom options
  custom_config = r'--oem 3 --psm 6'
  info = pytesseract.image_to_string(img, config=custom_config)
  results = []
  
  if type.lower() == "rappi":
    info =  info.split("\n")
    for index in range(0, len(info), 2):
      try:
        raw_date =  " ".join(info[index+1].split(" ")[:4])
        date = parse_date(raw_date)
        results.append(f'{date} {info[index].replace(".", "")}')
      except:
        try:
          raw_date =  " ".join(info[index+2].split(" ")[:4])
          date = parse_date(raw_date)
          results.append(f'{date} {info[index].replace(".", "")}')
        except:
          continue
        continue
  else:
    for texto in info.split("\n"):
      match = re.match(r'(\d{4}/\d{2}/\d{2})\s+(.*)\s+([-\d,]+)(\.\d{2})', texto)
      if match:
        fecha = match.group(1)
        descripcion = match.group(2).replace("IBAGUE", "").replace("BARBOSA", "").replace(" $", "")
        cantidad = match.group(3)

        # Formatear la fecha
        fecha_formateada = fecha[8:] + '/' + fecha[5:7] + '/' + fecha[0:4]
        cantidad_formateada = cantidad.replace("-", "").replace(',', '.')
        results.append(f"{fecha_formateada},{descripcion},{cantidad_formateada}")
  
  
  return "\n".join(results)

if __name__ == '__main__':
    print(main("."))
        
        