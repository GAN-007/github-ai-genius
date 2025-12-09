FROM golang:latest as builder

WORKDIR /go

COPY go.mod go.sum ./

RUN go mod download

COPY . .

RUN go build -o gitmal .

FROM alpine

COPY --from=builder /go/gitmal /bin/gitmal

WORKDIR /data

ENV COLORTERM=truecolor

ENTRYPOINT ["/bin/gitmal"]
