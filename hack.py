import math
import wlc
import requests
import apikey


w=wlc.Weblate(apikey.myAPIKey)
projects={'mobile':{},'server':{},'webapp':{},'glossary':{}}
projects['mobile']['shipped']='mattermost-mobile_master'
projects['mobile']['wip']='mattermost-mobile-wip'
projects['server']['shipped']='mattermost-server_master'
projects['server']['wip']='mattermost-server-wip'
projects['webapp']['shipped']='mattermost-webapp_master'
projects['webapp']['wip']='mattermost-webapp-wip'
projects['glossary']['shipped']='glossary'
projects['glossary']['wip']='glossary'

for project in projects:
  shippedLanguages={}
  WIPLanguages={}
### GETTING THE SHIPPED LANGUAGES ###
  print('GETTING SHIPPED LANGUAGES FOR '+project)
  shippedProjects=w.get('https://translate.mattermost.com/api/components/mattermost/'+projects[project]['shipped']+'/translations/')
  for shippedLanguage in shippedProjects['results']:
    if shippedLanguage['language']['code']=='en':
      continue
    shippedLanguageCode=shippedLanguage['language']['code']
    shippedLanguageName=shippedLanguage['language']['name']
    shippedLanguages[shippedLanguageCode]=shippedLanguageName

### GETTING THE WIP LANGUAGES ###
  print('GETTING WIP LANGUAGES FOR '+project)
  page=1
  next='https://translate.mattermost.com/api/components/i18n-wip/'+projects[project]['wip']+'/translations/'
  WIPProjects=w.get(next)
  lastpage=math.ceil(WIPProjects['count']/20)
  while page<=lastpage:   
    next='https://translate.mattermost.com/api/components/i18n-wip/'+projects[project]['wip']+'/translations/?page='+str(page)
    WIPProjects=w.get(next)
    page=page+1
    for WIPLanguage in WIPProjects['results']:
      if WIPLanguage['language']['code']=='en':
        continue
      WIPLanguageCode=WIPLanguage['language']['code']
      WIPLanguageName=WIPLanguage['language']['name']
      WIPLanguages[WIPLanguageCode]=WIPLanguageName

### GETTING REMOVING THE WIP LANGUAGES THAT ARE ALREADY IN SHIPPED ###
  print("*********************************")
  print(shippedLanguages.keys());
  print(WIPLanguages.keys());
  for languageToRemove in shippedLanguages.keys() & WIPLanguages.keys():
    print('REMOVING LANGUAGE '+languageToRemove +' FOR '+project)  
    try:
      headers = {'Content-Type': 'application/json',}
      values = '{ "text": "Removing '+languageToRemove+' from '+project+'"}'
      response = requests.post(apikey.myWebhook,headers=headers,data=values)
      r=w.request('delete','https://translate.mattermost.com/api/translations/i18n-wip/'+projects[project]['wip']+'/'+languageToRemove+'/')
    except:
      print ('Oops https://translate.mattermost.com/api/translations/i18n-wip/'+projects[project]['wip']+'/'+languageToRemove+'/')
    finally:
      print('more oops')

