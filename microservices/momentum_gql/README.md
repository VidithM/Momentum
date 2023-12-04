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

Some (new) sample commands:

```graphql
mutation{
  create_community(input:{
    description: "nmcclaran"

  })

  {
    error{
      description
    }
    community{
      rid
    }
  }
}

mutation{
  update_community(input:{
    rid: "656d17550f313512c360703a"
    description: "nmcclaran"
    users: []

  })

  {
    error{
      description
    }
    community{
      rid
      description
      posts
      {
        rid
      }
      }
    }
  }

  query{
  search_communities(terms:{
  descriptions: ["nmcclaran"]

  })
  {
    communities
    {
      rid
      users
      {
        rid
      }
      posts
      {
        rid
      }

    }
  }
}

mutation{
  create_post(input:{
    content: "nmcclaran_2"
    community: "656d15b40f313512c360702a"
    user: 17
    timestamp: "2023-09-29 22:41:58.235205"
  })

  {
    error{
      description
    }
    post{
      rid
      community
      {
        rid
      }
      }
    }
  }


mutation{
  create_user(input:{
    rid:17
    username: "nmcclaran17"
    password: "password"
    name: "Nathan"
    email: "nmcclaran17@tamu.edu"

  })

  {
    error{
      description
    }
    user{
      username
      email
      password
    }
  }
}

mutation{
  update_user(input:{
    rid: 1
    username: "nmcclaran"
    password: "password"
    name: "Nathan McClaran The Second"
    email: "nmcclaran2@tamu.edu"
    communities: ["656d175c0f313512c360703d", "656d15b40f313512c360702a", "656e30ce41cdcef847257e8e"]

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
    }
  }
}

query{
  search_users(terms:{
    rids: [12]


  })
  {
    users
    {
      rid
      email
      communities
      {
        rid
      }
    }
  }
}

mutation{
  create_comment(input:{
    parent: 1
    user:12
    content: "nmcclaran_3"
    timestamp: "2023-09-29 22:41:58.235205"
  })

  {
    error{
      description
    }
    comment{
      rid
    }
    }
  }

  query{
  search_posts(terms:{
    rids: [11]
  })

  {
    error{
      description
    }
    posts{
      rid
      comments
        {
          rid
          comments
          {
            parent
            {
              rid
            }
          }
     parent{
            rid
          }
        }
    }

    }
  }


```

Some (old) sample commands:

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
    rid: "rid"
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
