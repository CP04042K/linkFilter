# linkFilter
i came into a situation where i have to find away to process an enormous amount of url, which is result from tools like gospider, waybackurls. This is the script i created for my personal use, to make life easier for me

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
