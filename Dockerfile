FROM golang:1.22

ARG PORT
ENV PORT=${PORT}

ARG REGION
ENV REGION=${REGION}

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY main.go ./

EXPOSE $PORT

RUN CGO_ENABLED=0 GOOS=linux go build -o /fs_file_scanner

CMD ["/fs_file_scanner"]