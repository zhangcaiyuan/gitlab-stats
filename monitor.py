import json

import requests

from config import GITLAB_URL, GITLAB_TOKEN, GITLAB_USER


def get_issues_html(created_after: str = "2021-03-10"):
    """

    :return:
    """

    query = '''
        {
          users(usernames: ["''' + GITLAB_USER + '''"]) {
            nodes {
              name
              todos {
                edges {
                  node {
                    id
                  }
                }
              }
              groupMemberships {
                nodes {
                  createdAt
                  group {
                    fullName
                    issues(createdAfter:"''' + created_after + '''") {
                      nodes {
                        assignees {
                         nodes{
                          name
                        }
                        }
                        discussions {
                          nodes{
                            createdAt
                            notes {
                              nodes {
                                body
                                author {
                                  name
                                }
                              }
                            }
                          }
                        }
                        title
                        description
                        author {
                          name
                        }
                        currentUserTodos {
                          nodes {
                            author {
                              name
                            }
                            state
                          }
                        }
                        state
                        createdAt
                        closedAt
                        dueDate
                        type
                        milestone {
                          title
                          description
                          dueDate
                          startDate
                        }
                        labels {
                          nodes {
                            title
                          }
                        }
                      }
                    }
                  }
                  user {
                    name
                  }
                }
              }
            }
          }
        }
    '''

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GITLAB_TOKEN}"
    }

    result = requests.post(
        url=f"{GITLAB_URL}/api/graphql",
        data=json.dumps({"query": query}),
        headers=headers
    )

    if result.status_code == 200:
        result = json.loads(result.content)

        groups = [gm["group"] for gm in result["data"]["users"]["nodes"][0]["groupMemberships"]["nodes"]]
        content = """<table border="1">"""
        content += """<tr>
                    <th>项目名称</th>
                    <th>issue名称</th>
                    <th >issue描述</th>
                    <th>issue所属人</th>
                    <th>issue状态</th>
                    <th>issue创建时间</th>
                    <th>issue截止时间</th>
                    <th>issue关闭时间</th>
                    <th>issue标签</th>
                    <th>issue里程碑</th>
                    <th>issue里程碑描述</th>
                    <th>issue里程碑开始时间</th>
                    <th>issue里程碑结束时</th>
                    <th>issue指派人</th>
                    <th>issue评论</th>
                    </tr>"""
        for group in groups:
            # group.fullName
            full_name = group["fullName"]
            # group.issues
            issues = group["issues"]["nodes"]
            for issue in issues:
                # issue.title
                title = issue["title"]
                # issue.description
                description = issue["description"]
                # issue.author
                author = issue["author"]["name"]
                # issue.state
                state = issue["state"]
                # issue.createdAt
                created_time = issue["createdAt"]
                # issue.dueDate
                due_date = issue["dueDate"]
                # issue.closedAt
                closed_time = issue["closedAt"]
                # timeout

                # issue.labels
                labels = [label["title"] for label in issue["labels"]["nodes"]]
                # issue.milestone
                milestone = issue["milestone"]
                milestone_title = ""
                milestone_description = ""
                milestone_start_date = ""
                milestone_due_date = ""
                if milestone:
                    milestone_title = milestone["title"]
                    milestone_description = milestone["description"]
                    milestone_start_date = milestone["startDate"]
                    milestone_due_date = milestone["dueDate"]
                # issue.assignees
                assignees = [user["name"] for user in issue["assignees"]["nodes"]]
                # issue.discussions
                discussions = [dis["notes"]["nodes"] for dis in issue["discussions"]["nodes"]]

                content += f"""<tr>
                    <td>{full_name}</td>
                    <td>{title}</td>
                    <td>{description}</td>
                    <td>{author}</td>
                    <td>{state}</td>
                    <td>{created_time}</td>
                    <td>{due_date}</td>
                    <td>{closed_time}</td>
                    <td>{','.join(labels)}</td>
                    <td>{milestone_title}</td>
                    <td>{milestone_description}</td>
                    <td>{milestone_start_date}</td>
                    <td>{milestone_due_date}</td>
                    <td>{','.join(assignees)}</td>
                    <td>{discussions}</td>
                    """
        content += "</table>"
    else:
        content = result.content
    return content


def get_issues_list(created_after: str = "2021-03-10"):
    """

    :return:
    """

    query = '''
        {
          users(usernames: ["''' + GITLAB_USER + '''"]) {
            nodes {
              name
              todos {
                edges {
                  node {
                    id
                  }
                }
              }
              groupMemberships {
                nodes {
                  createdAt
                  group {
                    fullName
                    issues(createdAfter:"''' + created_after + '''") {
                      nodes {
                        assignees {
                         nodes{
                          name
                        }
                        }
                        discussions {
                          nodes{
                            createdAt
                            notes {
                              nodes {
                                body
                                author {
                                  name
                                }
                              }
                            }
                          }
                        }
                        title
                        description
                        author {
                          name
                        }
                        currentUserTodos {
                          nodes {
                            author {
                              name
                            }
                            state
                          }
                        }
                        state
                        createdAt
                        closedAt
                        dueDate
                        type
                        milestone {
                          title
                          description
                          dueDate
                          startDate
                        }
                        labels {
                          nodes {
                            title
                          }
                        }
                      }
                    }
                  }
                  user {
                    name
                  }
                }
              }
            }
          }
        }
    '''

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GITLAB_TOKEN}"
    }

    result = requests.post(
        url=f"{GITLAB_URL}/api/graphql",
        data=json.dumps({"query": query}),
        headers=headers
    )
    issue_list = []
    if result.status_code == 200:

        result = json.loads(result.content)

        groups = [gm["group"] for gm in result["data"]["users"]["nodes"][0]["groupMemberships"]["nodes"]]

        for group in groups:
            # group.fullName
            full_name = group["fullName"]
            # group.issues
            issues = group["issues"]["nodes"]
            for issue in issues:

                issue_obj = {}

                # issue.title
                title = issue["title"]
                # issue.description
                description = issue["description"]
                # issue.author
                author = issue["author"]["name"]
                # issue.state
                state = issue["state"]
                # issue.createdAt
                created_time = issue["createdAt"]
                # issue.dueDate
                due_date = issue["dueDate"]
                # issue.closedAt
                closed_time = issue["closedAt"]
                # timeout

                # issue.labels
                labels = [label["title"] for label in issue["labels"]["nodes"]]
                # issue.milestone
                milestone = issue["milestone"]
                milestone_title = ""
                milestone_description = ""
                milestone_start_date = ""
                milestone_due_date = ""
                if milestone:
                    milestone_title = milestone["title"]
                    milestone_description = milestone["description"]
                    milestone_start_date = milestone["startDate"]
                    milestone_due_date = milestone["dueDate"]
                # issue.assignees
                assignees = [user["name"] for user in issue["assignees"]["nodes"]]
                # issue.discussions
                discussions = [dis["notes"]["nodes"] for dis in issue["discussions"]["nodes"]]

                issue_obj["project_name"] = full_name
                issue_obj["title"] = title
                issue_obj["description"] = description
                issue_obj["author"] = author
                issue_obj["state"] = state
                issue_obj["assignees"] = ','.join(assignees)
                issue_obj["created_time"] = created_time
                issue_obj["due_date"] = due_date
                issue_obj["closed_time"] = closed_time
                issue_obj["labels"] = ','.join(labels)
                issue_obj["milestone_title"] = milestone_title
                issue_obj["milestone_description"] = milestone_description
                issue_obj["milestone_start_date"] = milestone_start_date
                issue_obj["milestone_due_date"] = milestone_due_date
                issue_obj["discussions"] = discussions
                issue_list.append(issue_obj)
    return issue_list











