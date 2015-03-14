import qrcode
import qrcode.image.svg
from os import path, makedirs
from shutil import copyfile
from urllib.parse import urljoin
from tornado.template import Template

def generate(codes, output_path = './qrmaster',
             url='http://test.com', title='',
             img_path=None):
    
    module_path, _ = path.split(__file__)
    css_file_name = 'style.css'
    
    template_path = path.join(module_path, 'template.html')
    css_path = path.join(module_path, css_file_name)
    
    output_file = path.join(output_path, 'qrmaster.html')
    o_css_path = path.join(output_path, css_file_name)
    
    files_path = path.join(output_path, 'qrmaster')
    if not path.exists(files_path):
        makedirs(files_path)
    
    if img_path:
        _, img_file_name = path.split(img_path)
        o_img_path = path.join(output_path, img_file_name)
        copyfile(img_path, o_img_path)
    else:
        o_img_path = ''
    
    copyfile(css_path, o_css_path)
        
    urls = {}
    for c in codes:
        qr = qrcode.QRCode(
            version = 1,
            box_size = 5,
            border = 0,
            error_correction=
                qrcode.constants.ERROR_CORRECT_H,
        )
        full_url = urljoin(url, c)
        urls[c] = full_url
        qr.add_data(full_url)
        qr.make()
        qr_path = path.join(files_path, c+'.svg')
        qr.make_image(
            image_factory=qrcode.image.svg.SvgImage).save(
                qr_path)

    with open(template_path, 'r') as f:
        tmp = f.read()
        
    html = Template(tmp).generate(urls=urls,
        files_path=files_path, title=title,
        img_path=img_file_name)
    
    with open(output_file, 'w') as f:
        f.write(
            html.decode('utf-8')
        )
