import requests
import re

RAW_CONTENT_URL = 'https://raw.githubusercontent.com/sologuboved/{reponame}/master/{fname}'
REPO_CONTENT_URL = 'https://api.github.com/repos/sologuboved/{reponame}/contents/'
RAW_PREFIX = 'raw_'
LABEL = "Scraping {reponame}..."


def print_label(reponame):
    print('\n' + LABEL.format(reponame=reponame))


def collect_fnames(reponame):
    return [entry['name'] for entry in requests.get(REPO_CONTENT_URL.format(reponame=reponame)).json()]


def write_raw_file(url, fname):
    print(fname + ':', "writing raw...")
    with open(RAW_PREFIX + fname, 'wb') as handler:
        handler.write(requests.get(url).content)


def write_clean_file(fname):
    print(fname + ':', "writing clean...")
    with open(RAW_PREFIX + fname) as raw, open(fname, 'w') as clean:
        raw_line = True
        while raw_line:
            raw_line = raw.readline()
            clean.write(process_line(raw_line))


def process_line(raw_line):
    if raw_line == '\n':
        return ''
    clean_line = ''
    for char in raw_line:
        if char.isalpha():
            clean_line += char.lower()
        else:
            clean_line += ' '
    clean_line = (re.compile(r" +").sub(' ', clean_line)).strip() + ' '
    return clean_line


def scrape_files(py_fnames, reponame):
    for py_fname in py_fnames:
        txt_fname = py_fname[: -3] + '.txt'
        url = RAW_CONTENT_URL.format(reponame=reponame, fname=py_fname)
        write_raw_file(url, txt_fname)
        write_clean_file(txt_fname)


def scrape_goodreads():
    reponame = 'goodreads_py3'
    print_label(reponame)
    scrape_files(filter(lambda f: f.endswith('.py') and f.startswith('goodreads'), collect_fnames(reponame)), reponame)


def scrape_stubb():
    reponame = 'stubb'
    print_label(reponame)
    excl = {'update_top_tests.py', 'substitutes.py', 'check_if_fits.py'}
    scrape_files(filter(lambda f: f.endswith('.py') and f not in excl, collect_fnames(reponame)), reponame)


def scrape_timecalc():
    reponame = 'time_calc'
    print_label(reponame)
    excl = {'launch.py', 'global_vars.py'}
    scrape_files(filter(lambda f: f.endswith('.py') and f not in excl, collect_fnames(reponame)), reponame)


def scrape_small_repos():
    reponames = ['misc', 'pagecount', 'conferatur']
    for reponame in reponames:
        print_label(reponame)
        scrape_files(filter(lambda i: i.endswith('.py'), collect_fnames(reponame)), reponame)


if __name__ == '__main__':
    scrape_timecalc()
