# -*- coding: UTF-8 -*-

# COPYRIGHT (c) 2016 Cristóbal Ganter
#
# GNU AFFERO GENERAL PUBLIC LICENSE
#    Version 3, 19 November 2007
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import qrcode
import qrcode.image.svg
from os import path, makedirs
from shutil import copyfile
from urllib.parse import urljoin
from tornado.template import Template

def generate(codes, output_path = './qrmaster',
             url='http://test.com', title='',
             img_path=None):
    """codes are tuples in the form: (code, id)"""

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

    data = []
    for c in codes:
        qr = qrcode.QRCode(
            version = 1,
            box_size = 5,
            border = 0,
            error_correction =
                qrcode.constants.ERROR_CORRECT_H
        )
        full_url = urljoin(url, c[0])
        c.append(full_url)
        data.append(c)
        qr.add_data(full_url)
        qr.make()
        qr_path = path.join(files_path, c[0]+'.svg')
        qr.make_image(
            image_factory=qrcode.image.svg.SvgImage).save(
                qr_path)

    with open(template_path, 'r') as f:
        tmp = f.read()

    html = Template(tmp).generate(data=data,
                                  files_path=files_path,
                                  title=title,
                                  img_path=img_file_name)

    with open(output_file, 'w') as f:
        f.write(
            html.decode('utf-8')
        )
