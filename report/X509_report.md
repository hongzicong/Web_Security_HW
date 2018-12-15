

## 概述

X.509证书是用 ASN1 语法进行编码的数字证书标准

## ASN1

ASN1采用一个个的数据块来描述整个数据结构，每个数据块都有四个部分组成：



为了更好的理解 X.509 的结构，而不是 ASN1 的结构，所以在本次 X.509 实现中，我采用了 python 的 asn1 包来进行解析

## 证书结构

 - Certificate
    - Version
    - Serial Number
    - Algorithm ID
    - Issuer
    - Validity
        - Not Before
        - Not After
    - Subject
    - Subject Public Key Info
        - Public Key Algorithm
        - Subject Public Key
    - Issuer Unique Identifier (Optional)
    - Subject Unique Identifier (Optional)
    - Extensions (Optional)
    - Certificate Signature Algorithm
    - Certificate Signature


Download from:

http://fm4dd.com/openssl/certexamples.htm