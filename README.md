# AI Data Operations - Consumer
Consumidor AWS Lambda para processar eventos de e-commerce provenientes do Amazon Kinesis Data Streams , incluindo validação de eventos, enriquecimento de payload e persistencia de dados brutos no Amazon S3, com tratamento de erros confiável e recursos de reprocessamento.

O componente valida esquema de eventos, enriquece payloads de eventos com metadados de processamento e persiste eventos brutos no Amazon S3. Ele foi projetado com arquitetura modular, testes atutomatizados e recursos confiáveis de tratamento de erros.

## Architecture
```text
Amazon kinesis Data Streams
            |
            V
       AWS Lambda
            |
            V
    Event Processor
            |
            V
      +-----+-----+
      |           |
      v           v
  Validation    Enrichment
                  |
                  V
               Amazon S3
                Raw Data

Failure handling:
Amazon SQS (planned)