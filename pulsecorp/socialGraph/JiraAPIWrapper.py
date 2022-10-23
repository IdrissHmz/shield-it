from jira import JIRA
import requests
import json
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
class JiraException(Exception):
	pass
class Jira(object):
	__options = {
		'server':'https://xylexa.atlassian.net',
		'verify':False
	}
	__client = JIRA(__options, basic_auth=('muhammad.jahanzaib@xylexa.com', 'NmwZNfbAM3pTr5dtpIKO80EB'))
	#__client = JIRA(__options, basic_auth=('buisnoche@gmail.com', 'X8DHjJIlCCEzG7j52EXjD290'))
	def __init__(self, **kwargs):
		if self.__client == None:
			if len(kwargs) != 2:
				raise JiraException('In order to use this class you need to specify a user and a password as keyword arguments!')
			else:
				if 'username' in kwargs.keys():
					self.__username = kwargs['username']
				else:
					raise JiraException('You need to specify a username as keyword argument!')
				if 'password' in kwargs.keys():
					self.__password = kwargs['password']
				else:
					raise JiraException('You need to specify a password as keyword argument!')
				
				try:
					self.__client = JIRA(self.__options, basic_auth=(self.__username, self.__password))
				except:
					raise JiraException('Could not connect to the API, invalid username or password!') from None
	def __str__(self):
		return 'Jira(username = {}, password = {}, endpoint = {}'.format(self.__username, self.__password, self.__options['server'])

	def __repr__(self):
		return 'Jira(username = {}, password = {}, endpoint = {}'.format(self.__username, self.__password, self.__options['server'])

	def __format__(self, r):
		return 'Jira(username = {}, password = {}, endpoint = {}'.format(self.__username, self.__password, self.__options['server'])

	def getProjects(self, raw = False):
		Projects = []
		for project in self.__client.projects():
			if raw:
				Projects.append(project)
			else:
				Projects.append({ 'name':project.name, 'key':project.key, 'id':project.id })
		return Projects
	def getIssues(self, maxResults = 50, raw = False, **kwargs):
		Issues = []
		if len(kwargs) < 1:
			raise JiraException('You need to specify a search criteria!')
		else:
			searchstring = ' '.join([( _ + "=" + kwargs[_]) if _ != 'condition' else kwargs[_] for _ in kwargs])
			for item in self.__client.search_issues(searchstring):
				if raw:
					Issues.append(item)
					print(item.fields.timespent)
				else:
					Issues.append({
						'id':item.id,
						'assignee':item.fields.assignee,
						'timeSpent':item.fields.timespent,
						'createDate':item.fields.created,
						'dueDate':item.fields.duedate,
						'resolutionDate':item.fields.resolutiondate,
						'status':item.fields.status,
						# 'Peer Reviewer':item.fields.customfield_13307,
						'reporter':item.fields.reporter,
						'name':str(item), 
						'summary':item.fields.summary, 
						'description':item.fields.description
					})
		return Issues
	def transition(self, issue, transition):
		pass
	def new_issue(self, **kwargs):
		pass
	# def comment_issue(self, issue, comment)	

	def search_users(self, query, startAt=0, maxResults=50, includeActive=True, includeInactive=False):	
		auth = HTTPBasicAuth("muhammad.jahanzaib@xylexa.com", "NmwZNfbAM3pTr5dtpIKO80EB")
		headers = {"Accept": "application/json"}
		query = {'query': query}
		response = requests.request(
			"GET",
			'https://xylexa.atlassian.net//rest/api/2/user/search',
			headers=headers,
			params=query,
			auth=auth
		)
		# print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
		return response.json()
# if __name__ == '__main__':
# 	MyJira = Jira(username='MyUser', password='MyPassword')
# 	print(MyJira.getProjects())
# 	print(MyJira.getIssues(project='MyProject',condition='AND',status='Closed')) 

# options = {"server": "https://xylexa.atlassian.net"}
# jira = JIRA(basic_auth=("muhammad.jahanzaib@xylexa.com", "NmwZNfbAM3pTr5dtpIKO80EB"), options=options)  # a username/password tuple
# print(jira.projects())