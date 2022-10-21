import os
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Point to Hasura and pass in the admin secret
transport = AIOHTTPTransport(url="https://gql.rcos.io/v1/graphql", headers={
    "content-type": "application/json", "x-hasura-admin-secret": os.environ.get('HASURA_SECRET') 
})

# Create a GraphQL client
client = Client(transport=transport, fetch_schema_from_transport=True)

def get_project(project_id: str):
    query = gql("""
        query GetProject($id: Int!) {
          projects(where: {project_id: {_eq: $id}}) {
            title
            description
            stack
            repository_urls
            project_id
          }
        }

    """)

    result = client.execute(query, variable_values={ "id": project_id })
    return result["projects"]

def get_semester_projects(semester: str, with_enrollments: bool):
    query = gql("""
        query SemesterProjects($semesterIdOrTitle: String!, $withEnrollments: Boolean!) {
            projects(order_by: {title: asc}, where: {enrollments: {_or: [{semester_id: {_eq: $semesterIdOrTitle}}, {semester: {title: {_ilike: $semesterIdOrTitle}}}]}}) {
                project_id
                title
                enrollments @include(if: $withEnrollments) {
                user {
                    id
                    first_name
                    last_name
                    cohort
                }
                is_project_lead
                credits
                is_for_pay
                }
            }
        }
    """)

    result = client.execute(query, variable_values={"semesterIdOrTitle": semester, "withEnrollments": with_enrollments})
    return result["projects"]

