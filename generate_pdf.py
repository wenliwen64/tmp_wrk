import jinja2
import os
from jinja2 import Template
from subprocess import Popen
from sklearn.datasets import load_iris
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def compile_tex(tex_file_path, out_pdf_path):
    # $pdflatex /path/to/xxxx.tex -job-name out -output-directory /abs/path/to/out/dir
    p = Popen(['pdflatex', tex_file_path, '-job-name', 'out', '-output-directory', os.path.dirname(out_pdf_path)])
    p.communicate()

def main():
    latex_jinja_env = jinja2.Environment(
            block_start_string = '\BLOCK{',
            block_end_string = '}',
            variable_start_string = '\VAR{',
            variable_end_string = '}',
            comment_start_string = '\#{',
            comment_end_string = '}',
            line_statement_prefix = '%%',
            line_comment_prefix = '%#',
            trim_blocks = True,
            autoescape = False,
            loader = jinja2.FileSystemLoader(os.path.abspath('/'))
            )
    tex_file_path = './template.tex'
    out_pdf_path = './out.pdf'

    iris = load_iris()
    iris_df = pd.DataFrame(data=np.c_[iris['data'], iris['target']], columns=['SepalLen', 'SepalWid', 'PetalLen', 'PetalWid', 'target'])
    template = latex_jinja_env.get_template(os.path.realpath('./template.tex'))

    # generate figures
    figures = []
    for col in iris_df.columns[:-1]:
       fig, ax = plt.subplots()
       ax.plot(iris_df[col])
       fig.savefig(f'./{col}.pdf')
       figures.append((f'./{col}.pdf', col))

    iris_sub_dfs = np.split(iris_df, [int(.3 * len(iris_df)), int(.6 * len(iris_df))])
    print(iris_sub_dfs[2])
    print([int(.3 * len(iris_df)), int(.3 * len(iris_df))])
    renderer = template.render(dfs=iris_sub_dfs, figs=figures, len=len)

    with open('./out.tex', 'w') as renderer_file:
        renderer_file.write(renderer)
    #print(iris_df)

    compile_tex(tex_file_path='./out.tex', out_pdf_path='./')

if __name__ == '__main__':
    main()
