# GraphQL App

## Local development

Create a virtual environment and install the project in
dev mode by using the venv target in the Makefile.

```bash
make venv
source .venv/bin/activate
```

## Run

### Setup Environment

```bash
source .venv/bin/activate
make requirements
pip install -e ".[dev]"
pip install -r requirements

```

### Run the application

While in the top level directory (and in virtual environment)

`python -m app --port=8020`

### Run the Sequel Server

```bash
docker compose up
```

The commands for creating the tables are under the python create_table funciton in the database folder.

### Playground

Navigate to localhost:8020 to interact with the playground.

Otherwise, post to localhost:8020 a proper gql request.

Some sample commands:

```graphql
query{
  search_communities(terms:{
    rids:[1,2,3]

  })
  {
    communities
    {
      rid
    }
  }
}

mutation{
  update_comment(input:{
    rid: 11
    content: "nmcclaran_3"
    timestamp: "2023-09-29 22:41:58.235205"
  })

  {
    error{
      description
    }
    comment{
      rid
      parent{
        rid
        comments
        {
          rid
        }
        }
      }
    }
  }

mutation{
  update_post(input:{
    rid: 1
    content: "nmcclaran_3"
  })

  {
    error{
      description
    }
    post{
      rid
      user{
        rid
      }
        }
      }
    }

mutation{
  create_post(input:{
    content: "nmcclaran_2"
    community: 17
    user: 17
    timestamp: "2023-09-29 22:41:58.235205"
  })

  {
    error{
      description
    }
    post{
      rid
      user{
        name
        posts
        {
          rid
        }
        }
      }
    }
  }

mutation{
  update_community(input:{
    rid: 17
    description: "nmcclaran_2"
    users: [17]

  })

  {
    error{
      description
    }
    community{
      rid
      posts
      {
        rid
      }
      }
    }
  }

mutation{
  create_community(input:{
    description: "nmcclaran"
    users: [17]

  })

  {
    error{
      description
    }
    community{
      rid
      users{
        name
      }
    }
  }
}

mutation{
  update_user(input:{
    rid: 17
    username: "nmcclaran"
    password: "password"
    name: "Nathan McClaran"
    email: "nmcclaran@tamu.edu"

  })

  {
    error{
      description
    }
    user{
      rid
      username
      email
      password
      name
      posts
      {
        rid
      }
    }
  }
}


mutation{
  create_user(input:{
    username: "nmcclaran"
    password: "password"
    name: "Nathan"
    email: "nmcclaran@tamu.edu"

  })

  {
    error{
      description
    }
    user{
      rid
      username
      email
      password
    }
  }
}
```

### Bugs

Sometimes the gql calls fail if you go too far down the nested dependency tree.  Probably due to me not closing cursors.  I'll fix it sometime.
