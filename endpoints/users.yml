---
enabled: true
endpoint: users
info: This endpoint is for saving and restoring users.

CREATE:
  - op: create
    query:
      datastore: MySQL
      op: INSERT INTO users (name, age, hobbies) VALUES (%s, %s, %s)
      params:
      - "{{ url.name }}"
      - "{{ url.age }}"
      - "{{ url.hobbies  }}"

