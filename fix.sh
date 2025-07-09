#!/usr/bin/bash

sed -E ':a; s/^(([^\t]*\t){8}[^\t]*)(\t+)/\1 /; ta'  dm.raw.gff |grep -v -P '\tregion\t' > dm.gff
sed -E ':a; s/^(([^\t]*\t){8}[^\t]*)(\t+)/\1 /; ta'  at.raw.gff |grep -v -P '\tregion\t' > at.gff
sed -E ':a; s/^(([^\t]*\t){8}[^\t]*)(\t+)/\1 /; ta'  hs.raw.gff |grep -v -P '\tregion\t' > hs.gff
