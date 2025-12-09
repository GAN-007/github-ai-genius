<p align="center"><img src="img/github-ai-genius-color-logo.webp" alt="GitHub AI Genius" width="330" height="330"></p>

# GitHub AI Genius

GitHub AI Genius is a static page generator for Git repositories. GitHub AI Genius generates static HTML pages with files, commits,
code highlighting, and markdown rendering.

## Installation

```sh
go install github.com/antonmedv/github-ai-genius@latest
```

```sh
docker run --rm -v $(pwd):/repo antonmedv/github-ai-genius /repo
```

Or download prebuilt binary from [releases](https://github.com/antonmedv/github-ai-genius/releases).

## Usage

Run github-ai-genius in the repository dir. GitHub AI Genius will generate pages in _./output_ directory.

```sh
github-ai-genius .
```

Run github-ai-genius with `--help` flag, go get a list of available options.

```sh
github-ai-genius --help
```

## Screenshots

<p align="center">
  <a href="img/github-ai-genius-screenshot-code-highlighting.webp"><img src="img/github-ai-genius-screenshot-code-highlighting.webp" alt="GitHub AI Genius Code Highlighting" width="400"></a>
  <a href="img/github-ai-genius-screenshot-file-tree.webp"><img src="img/github-ai-genius-screenshot-file-tree.webp" alt="GitHub AI Genius File Tree" width="400"></a><br>
  <a href="img/github-ai-genius-screenshot-files.webp"><img src="img/github-ai-genius-screenshot-files.webp" alt="GitHub AI Genius Files Page" width="400"></a>
</p>

## Examples

Here are a few examples of repos hosted on my website:

- [git.medv.io/zx/](https://git.medv.io/zx/) — github.com/google/zx
- [git.medv.io/zig/](https://git.medv.io/zig/) — codeberg.org/ziglang/zig (light theme)
- [git.medv.io/my-badges/](https://git.medv.io/my-badges/) — github.com/my-badges/my-badges

GitHub AI Genius on kubernetes repository works as well. Generation on my MacBook Air M2 with `--minify` and `--gzip` flags
takes around 25 minutes, and the generated files weigh around 2 GB.

## Themes

GitHub AI Genius supports different code highlighting themes. You can customize the theme with `--theme` flag.

```sh
github-ai-genius --theme github-dark
```

## Documentation

- [How to Self-Host a Git Repository?](./docs/how-to-self-host-a-git-repository.md)

## License

[MIT](LICENSE)
