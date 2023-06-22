# scripts
Some scripts i create to make penetration testing easier for me, i don't invest much time on most of them so please feel free to commit your modification

getting subdomains from list:
```
echo -n "example.txt" | waybackurls > wayback.txt
linkFilter wayback.txt "domainonly=true" | sort -u > subdomains.txt
```
```
gospider -s https://example.txt/Pages/default.aspx > go.txt
linkFilter go.txt "domainonly=true" | sort -u > subdomains.txt
```
combine with fff of tomnomnom:
```
linkFilter result.txt "domainandprotocol=true" | sort -u | fff
```
resolve ip:
```
linkFilter g.txt "resolveip=onlyip"
```
to get associated hostname:
```
linkFilter g.txt "resolveip=true"
```
