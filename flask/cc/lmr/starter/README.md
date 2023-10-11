# Models

 - Left
    - **id**   Integer (primary key)
    - **column** String (unique, not null)
 - Middle
    - **id**        Integer (primary key)
    - **column**   String (not null)
    - **left_id** Integer (not null)
    - **right_id** Integer (not null)
 - right
    - **id**   (primary key)
    - **column** (unique, not null)
# Validation

  - Left
    - column must be letters only
  - Right
    - column must be digits only
  - Middle
    - column must be punctuation only
# Routes

  - GET /rights
  - GET /rights/<int:id>
  - POST /lefts
  - PATCH /middles/<int:id>
  - DELETE /lefts/<int:id>
    

# Response Formats

- GET /rights
    ```json
    [
        {
            id
            column
        }
    ]
- GET /rights/<int:id>
    ```json
    [
        {
            id
            column
            middles:[
                {
                    id
                    column
                    left_id
                    right_id
                    left:{
                        id
                        column
                    }
                }
            ]
        }
    ]
    ```
- POST /lefts
    ```json
        {
            id
            column
            middles:[
                {
                    id
                    column
                    right_id
                    left_id
                    right:{
                        id
                        column
                    }
                }

            ]
    ```
- PATCH /middles/<int:id>
    ```json
        {
            id
            left_id
            right_id
            column
        }
    ```