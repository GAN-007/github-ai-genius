# How to Self-Host a Git Repository?

**Goal**: self-host a Git repository on your server, allowing read-only clones and a web view.

Create a _git_ user on the server where you want to host the repository. This step is optional, but I like to use a
dedicated user for repository management to keep the system secure and organized.

Create a `~/public` directory, which will serve as the web root. Configure a web server to serve files from this
directory.

## Bare repo

Create a bare repository inside `~/public`.
A [bare repository](https://git-scm.com/book/en/v2/Git-on-the-Server-The-Protocols)
is a special type of Git repository that doesn't have a working directory. It's used for hosting and sharing code
without the need for a local working copy.

```sh
git init --bare repo.git
```

Create a [post-update](https://git-scm.com/docs/git-receive-pack#_post_update_hook) hook with the following content:

```sh
#!/bin/sh
exec git update-server-info
```

Make the hook executable:

```sh
chmod +x hooks/post-update
```

## Gitmal hook

Create a [post‑receive](https://git-scm.com/docs/git-receive-pack#_post_receive_hook) hook with the following content:

```sh
#!/bin/sh
exec gitmal --output /home/git/public/repo/
```

Make the hook executable:

```sh
chmod +x hooks/post-receive
```

## Publish

Push your local repository to the bare repository on the server using ssh protocol.

```sh
git remote add origin git@example.com:public/repo.git
git push origin master
```

After pushing, git will run gitmal and generate files under `~/public/repo/` directory.

- Private read-write clone URL: `git@example.com:public/repo.git`
- Public **read-only** clone URL: `http://example.com/repo.git`
- Gitmal static web view: `http://example.com/repo/`

```sh
git clone https://example.com/repo.git
```
