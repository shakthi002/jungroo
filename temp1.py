import re
import pytesseract
from PIL import Image
from Eng_hin import translate
from check_meaning  import check
import streamlit as st
import os  
import pyvips  
import textwrap  
from PIL import *  
import pandas as pd  
from PIL import Image  
from PIL import ImageFont  
from PIL import ImageDraw   
 
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def questionOnlyNoMcqs(path_to_image):
    '''
    Function to generate hindi text of question only image with no mcqs
    :param path_to_image: str
    :return: str
    '''
    image = Image.open(path_to_image)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    text = pytesseract.image_to_string(image)
    text = text.lower()
    new_text = re.sub("q\.\d+\.+[a-zA-Z]+", "", text)
    new_text = re.sub(r'[^\w\s]', '', new_text)
    new_text = new_text.split()
    exam_details = []
    for i in range(len(new_text)):
        if new_text[i] in ["cbse","state","icse","igcse"]:
               exam_details.append(new_text[i])
        elif new_text[i].isdigit() and int(new_text[i])>=1900:
              exam_details.append(new_text[i])
        elif new_text[i].isdigit() and new_text[i+1]=="marks":
                exam_details.append(new_text[i])
                exam_details.append(new_text[i+1])
        else:
            continue
        print(exam_details)
    for i in exam_details:
         new_text.remove(i)
    words = []
    for i in new_text:
         if i.isalpha():
              words.append(i)
    sentence = ""
    for i in words[:len(words)-1]:
         sentence+=i+" "
    sentence+=words[-1]
    print(sentence)
    return translate(sentence)

def questionWithMcqs(path_to_image):
    '''
    :param path_to_image:
    :return:
    '''
    image = Image.open(path_to_image)
    text = pytesseract.image_to_string(image)

    text = text.lower()
    # print(text)
    # newtext = re.sub("q\.\d+\.+[a-zA-Z]+", "", text)
    newtext = re.sub("q\.\d+", "", text)
    # print(newtext)
    newtext = newtext.split()
    arr = []
    options = []
    new = []
    i = 0
    while (i < len(newtext)):
        if newtext[i] in ['cbse', 'CBSE']:
            for i in range(i, len(newtext)):
                arr.append(newtext[i])
            break
        elif newtext[i] in ['a.', 'b.', 'c.', 'd.', 'e.', 'f.']:
            s = ''
            while i < len(newtext) - 1 and newtext[i + 1] not in ['a.', 'b.', 'c.', 'd.', 'e.', 'f.', 'cbse']:
                s += newtext[i + 1]
                s += ' '
                i += 1
            options.append(s)

        else:
            new.append(newtext[i])
        i += 1
    seperator = " "
    updated_text = seperator.join(new)
    updated_text=translate(updated_text)
    #print(updated_text)
    #print(options)
    # print(arr)
    new_options = []
    for i in range(len(options)):
        op = options[i].split()
        #print(op)
        s = ''
        for j in op:
            if j.isdigit():
                s += j
                s += ' '
            else:
                s += translate(j)
                s += ' '
        new_options.append(s)
    # print(new_options)
    return updated_text + '\n\n\n'+ 'A)'+new_options[0]+'\n'+'B)'+new_options[1]+'\n'+'C)'+new_options[2]+'\n'+'D)'+new_options[3]

def onlysolution(path_to_image):
    image = Image.open(path_to_image)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    text_actual = pytesseract.image_to_string(image)
	# print(text)
    text=text_actual
    newtext = re.sub("Solution:", "", text)
    newtext = re.sub(r'[^\w\s]', '', newtext)
	# newtext=re.s
    newtext=newtext.split()
	# print(newtext)
    updated_text=[]
    seperator=" "
    for i in newtext:
	    if check(i)==1:
                updated_text.append(i)
    print(updated_text)
    updated_text=seperator.join(updated_text)
    # updated_text =seperator.join(updated_text)
    
    hindi=translate(updated_text)
    return hindi
def questionwithsolution(path_to_image):
    image = Image.open(path_to_image)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    text = pytesseract.image_to_string(image)
    text = text.lower()
    new_text = re.sub("q\.\d+\.+[a-zA-Z]+", "", text)
    new_text = re.sub(r'[^\w\s]', '', new_text)
    new_text = new_text.split()
    exam_details = []
    for i in range(len(new_text)):
        if new_text[i] in ["cbse","state","icse","igcse"]:
               exam_details.append(new_text[i])
        elif new_text[i].isdigit() and int(new_text[i])>=1900:
              exam_details.append(new_text[i])
        elif new_text[i].isdigit() and new_text[i+1]=="marks":
                exam_details.append(new_text[i])
                exam_details.append(new_text[i+1])
        else:
            continue
        # print(exam_details)
    for i in exam_details:
         new_text.remove(i)
    qwords = []
    awords=[]
    flag=1
    # print(new_text)
    for i in new_text:
         if check(i)==1:
            if i=='solution':
                flag=0
            if flag==1:
                 qwords.append(i)
            if flag==0:
                 awords.append(i)
    print(awords)   
    sentence = ""
    for i in qwords[:len(qwords)-1]:
         sentence+=i+" "
    sentence+=qwords[-1]
    sentence1 = ""
    for i in awords[:len(awords)-1]:
         sentence1+=i+" "
    sentence1+=awords[-1]
    # print(sentence)
    # print(sentence1)
    sentence=translate(sentence)
    
    sentence1=translate(sentence1)
    return sentence+"\n\n\n"+sentence1
    

options = ['questionOnlyNoMcqs', 'questionWithMcqs', 'onlysolution','questionwithsolution']
selected_option = st.selectbox('Select an option', options)
st.write('You selected:', selected_option)

st.title('Image uploader')

uploaded_file = st.file_uploader('Choose an image', type=['jpg', 'jpeg', 'png'])

# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     st.image(image, caption='Uploaded image')
print(uploaded_file)
if st.button('Save image'):
        # Save the image to disk
        with open('uploaded_image.png', 'wb') as f:
            f.write(uploaded_file.read())

        # Display a success message
        st.success('Image saved')

path = 'uploaded_image.png'
if selected_option=='questionOnlyNoMcqs':
     text=questionOnlyNoMcqs(path)
elif selected_option=='questionWithMcqs':
     text=questionWithMcqs(path)
elif selected_option=='onlysolution':
     text=onlysolution(path)
else:
     text=questionwithsolution(path)
# text=selected_option('last_frame2.png')
# text = questionwithsolution('last_frame2.png')

 # MAKE A FUNCTION  
 
def bgoutput(filename, text):  

   rendered_text, feedback = pyvips.Image.text(text,   
                         font='Mangal', fontfile='Mangal Regular.ttf',   
                         width=400, height=400,   
                         autofit_dpi=True) 
 
   rendered_text = rendered_text.gravity('centre', 1500, 1500)  
   image = rendered_text.new_from_image([0, 0, 0]).bandjoin(rendered_text)  
   image.write_to_file(f'{filename}.png')  


 # GENERATE OUTPUT 1   
bgoutput('new', text)  

 # COMBINE OUTPUT 1 WITH BACKGROUND IMAGE  
img = Image.open('new.png')
b1 = Image.open('plain_image.png')  
img = img.resize((1000,450)) 
b1.paste(img,(0,0), mask=img)

 # GENERATE FINAL OUTPUT  
b1.save("final3.png")

out_img=Image.open('final3.png')
st.image(out_img, caption='Output Image')