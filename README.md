# Dynamic and Uniform Databank Engine (dude)

## What is dude?

**THIS PROJECT IS CURRENTLY A WORK IN PROGRESS**

**dude** is a microservice middleware for taking HTTP/JSON requests and transforming them in to database requests.

It is **not a database management system (DBMS)**.

Each **HTTP Endpoint** can have a **CREATE**, **READ**, **UPDATE** and **DELETE** method associated with it. These are defined in an **endpoint file** written in **YAML**.

### mandate component

Each of these methods may have a **mandate component**.

This is **required** if your query requires parameters.

This step ensures that the **HTTP/JSON data** is the **correct type** before passing it over to the **query**.

The **components** for **mandate**  are currently planned to be **cookies**, **headers**, **json** and **url**.

### query component

Each of these methods should have a **query component** that relates to a **Databank (bank)** the user wishes to amend.

So for example in the case of **MySQL** the user would specify the **INSERT**, **SELECT**, **UPDATE** and **DELETE** queries, and render their **params** in the in the **params component**.

### transform component

**READ** has a special component called **transform**, this is an array of **Operations (ops)** to **mutate** the **returned data**.

This process is to ensure the data is in the desired format before returning it to the **sender**.

<img src="./docs/dude%20-%20Inside%20an%20Endpoint%20-%20Mandate_Query_Transform.png?raw=true" width="500">

### Dynamic?

The **endpoints** are **data-driven**. In theory these files could be **hot-reloaded** without having to rebuild and redeploy the code.

### Uniform?

Each **endpoint** is defined in the exact same way. All follow the same pattern and in theory can all use the same code/classes. This has the side-effect of making the microservice compact.

### Databank Engine?

Each **dude** in theory could sit in front of **many banks**. These could be different database types such as **MySQL**, **MongoDB** or even something like **Solr** or **Elasticsearch**.

By adding **Database Drivers (drivers)** to **dude** these resources could be changed **transparently** without the application using **dude** knowing the nitty gritty details.

## Endpoint Components

### CREATE

### READ

### UPDATE

### DELETE

tbd

## Method Components

**dude** is currently in development so these features aren't implemented. This is more of a written reference to guide the development.

Prototypes of how I want to use these are here in [sample.yml](./sample.yaml)

### mandate

**In Development**

Composed of these sub components, which are pulled from the HTTP request:

* cookies
* headers
* json
* url

**mandate** will be used to **define the type** and **import variables** into the **query component**. If it isn't in the mandate it will not be passed on. This **enforces** some degree of **validation** on **every variable**.

If the data can not be coerced in to the right format, **dude** should return an error and highlight the issue to the caller.

Below is an **example** of how I want the **mandate component** to look and feel.

```yaml
READ:
  mandate:
    cookies:
      # components
    headers:
      # that
    json:
      # specify
    url:
      # data format
```

#### str

If the type is set to **str** the value of what is in the parameter will be converted to a **str**. The components below are additional forms of validation.

##### contains

Has two required components. **op** and **values**. This component is a **list** of **dicts**.

**values** is a list of substrings to check against the **str**.

**op** can either be **accept** or **deny**. If the substring in values are found this value decides whether if the validation passes or not.

```yaml
READ:
  mandate:
    json:
      member:
        type: "str"
        contains:
        - op: 'accept'
          values:
          - "list"
          - "of"
          - "patterns"
```

##### re.search

Has two required components. **op** and **values**. This component is a **list** of **dicts**.

**values** is a list of **regular expressions** to check against the **str**. It is a wrapper around (https://docs.python.org/3/library/re.html).

**op** can either be **accept** or **deny**. If the substring in values are found this value decides whether if the validation passes or not.

```yaml
READ:
  mandate:
    json:
      member:
        type: "str"
        re.search:
        - op: 'deny'
          values:
          - ^hello
          - world$
```

##### deny

For anything more sophisticated the **deny** component can be used.

This is simply a list of expressions, and if they are true the validation will be denied. This may be a little slower, as it will require some string interpolation and jinja2 rendering.

**this** will be passed to the renderer as the current **str**.

```yaml
READ:
  mandate:
    json:
      member:
        type: "str"
        deny:
        - len(this) < 1
        - len(this) > 255
```

### query

**In Development**

Current **drivers** are:

* MySQL

#### MySQL

Current MySQL endpoint query component:

```yaml
    query:
      databank: MySQL
      op: INSERT INTO users (name, age, hobbies) VALUES (%s, %s, %s)
      params:
      - "{{ url.name }}"
      - "{{ url.age }}"
      - "{{ url.hobbies  }}"
```

Example MySQL Databank:

```yaml
bank: my_company
driver: MySQL
login:
  host: 127.0.0.1
  user: root
  passwd: "+zQx57?4$9"
```

### transform

**In Development**

## Unit Tests

There are unittests in the tests directory. To setup a testing environment you'll require **docker** and **docker-compose**.

Once in place you can use `docker-compose up -d` in the tests directory to bring up the environment.

## License

```
Copyright (c) 2019, Myke Atkinson
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the dude project.
```

