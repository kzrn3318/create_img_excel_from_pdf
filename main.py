import PyPDF2
from PIL import Image
import sys,os
import glob
import fitz
import camelot
import pandas as pd

def create_dir(img_dir , pdf_dir , excel_dir):
    img_dir_glob = glob.glob(str(img_dir))
    pdf_dir_glob = glob.glob(str(pdf_dir))
    excel_dir_glob = glob.glob(str(excel_dir))
    
    if len(pdf_dir_glob) > 0:
        pass
    else:
       os.mkdir(str(pdf_dir))
       
    if len(img_dir_glob) > 0:
        pass
    else:
        os.mkdir(str(img_dir))
    
    if len(excel_dir_glob) > 0:
        pass
    else:
        os.mkdir(str(excel_dir))
        

def create_page_pdf(pdf,page_count,pdf_dir):
    pdf_writer = PyPDF2.PdfFileWriter()
    pdf_writer.addPage(pdf.getPage(page_count))
    
    with open(".\\"+str(pdf_dir)+"\pdf{}.pdf".format(page_count),"wb") as f:
        pdf_writer.write(f)
    

def create_png(pdf_path,page_count,img_dir):
    pdf  = fitz.open(pdf_path)
    for num in range(len(pdf)):
        num_count = 0
        for image in pdf.getPageImageList(num):
            num_count += 1
            xref = image[0]
            pix = fitz.Pixmap(pdf,xref)
            
            if pix.n < 5:
                pix.writePNG(".\\"+str(img_dir)+"\img{}_{}.png".format(page_count,num_count))
            else:
                pix = fitz.Pixmap(fitz.csRGB,xref)
                pix.writePNG(".\\"+str(img_dir)+"\img{}_{}.png".format(page_count,num_count))
            
            pix = None
    
    pdf.close()
    
    
def create_excel(pdf_path,excel_dir,data_count):
    
    datas = camelot.read_pdf(pdf_path,split_text=True)
    data_count = data_count
    for data in datas:
        data_count += 1
        df =  data.df
        with pd.ExcelWriter(".\\"+str(excel_dir)+"\\from_pdf_{}.xlsx".format(data_count)) as file:
            df.to_excel(file,sheet_name="sheet1",index=False,header=False)
    return data_count


if __name__ == "__main__":
    args = sys.argv
    print([i for i in args])
    if len(args) >= 5:
        print("引数を受け取りました。")
        pdf_file = args[1]
        pdf_dir = args[2]
        img_dir = args[3]
        excel_dir = args[4]
    else:
        try:
            pdf_file = args[1]
            print("引数に指定がなかったため、デフォルト値で実行します。")
        except:
            raise ValueError("少なくとも一つのpdfのfileを引数とする必要があります。出力ディレクトリを指定する場合4つの引数を指定します。")
        pdf_dir ="pdf_list"
        img_dir="img_list"
        excel_dir="excel_data"
    
    pdf = PyPDF2.PdfFileReader(pdf_file)
    
    print("画像のディレクトリ:"+str(img_dir))
    print("pdf各ページのディレクトリ:"+str(pdf_dir))
    print("エクセルのデータディレクトリ:"+str(excel_dir))
    
    create_dir(img_dir,pdf_dir,excel_dir)
    
    page_count = 0
    for page in pdf.pages:
        create_page_pdf(pdf,page_count,pdf_dir)
        page_count += 1
        
    path_list = glob.glob(".\\"+pdf_dir+"\*.pdf")
    page_count = 0
    data_count = 0
    for path in path_list:
        page_count += 1
        create_png(path,page_count,img_dir)
        data_count = create_excel(path,excel_dir,data_count)
        
    print("処理終了\n")
    