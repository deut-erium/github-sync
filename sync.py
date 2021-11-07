import requests
import getpass
import os

PUB_ONLY = True
USERNAME = input('enter username:\n')
PASSWORD = ''
REPOSITORIES_PATH = ''
if input('update private repos too? y/n\n').lower()=='y':
    PASSWORD = getpass.getpass()
    PUB_ONLY=False

def get_repo_list():
    url = "https://api.github.com/search/repositories?q=user:{}"
    r = requests.get(url.format(USERNAME),auth=(USERNAME,PASSWORD))
    if r.status_code==200:
        repo_info = r.json()
        repo_priv, repo_pub = [],[]
        for repo_stats in repo_info['items']:
            if repo_stats['private']:
                repo_priv.append({i:repo_stats[i] for i in ('name','full_name')})
            else:
                repo_pub.append({i:repo_stats[i] for i in ('name','full_name')})
        return repo_pub, repo_priv

def check_and_fetch(repo_info):
    repo_path = os.path.join(REPOSITORIES_PATH,repo_info['name'])
    if not os.path.exists(repo_path):
        url = "https://{}:{}@github.com/{}.git".format(USERNAME,PASSWORD,repo_info['full_name'])
        os.system('git clone {}'.format(url))
    else:
        os.system('git -C {} pull'.format(repo_path))


pub_repos, priv_repos = get_repo_list()
npub,npriv = len(pub_repos), len(priv_repos)
for i,repo_info in enumerate(pub_repos):
    print('updating {}/{}'.format(i+1,npub))
    check_and_fetch(repo_info)

for i,repo_info in enumerate(priv_repos):
    print('updating {}/{}'.format(i+1,npriv))
    check_and_fetch(repo_info)

            
