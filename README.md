## Duck Duck API Server

---

[![codecov](https://codecov.io/gh/duck-duck-project/api-server/graph/badge.svg?token=FOYRAFGJWY)](https://codecov.io/gh/duck-duck-project/api-server)
[![Test](https://github.com/duck-duck-project/api-server/actions/workflows/unittests.yaml/badge.svg)](https://github.com/duck-duck-project/api-server/actions/workflows/unittests.yaml)
![Python](https://camo.githubusercontent.com/449440850ba7a1fc6a2c78a4fe05a5ccc9fddc05a46b85aa17f9f8cf657cb73c/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d332e31312d627269676874677265656e)

---

### Run postgresql in docker

```shell
docker run --name postgresql -e POSTGRES_USER=myusername -e POSTGRES_PASSWORD=mypassword -p 5432:5432 postgres
```