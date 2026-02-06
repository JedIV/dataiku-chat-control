# Connection Errors

## "Connection refused"
```
requests.exceptions.ConnectionError: Connection refused
```

**Causes:**
- Wrong DSS_URL
- Dataiku instance is down
- Network/firewall blocking

**Solutions:**
1. Verify URL: `echo $DSS_URL`
2. Test in browser: visit the URL
3. Check VPN if required
4. Ping the host

## "401 Unauthorized"
```
dataikuapi.utils.DataikuException: Unauthorized
```

**Causes:**
- Invalid API key
- API key expired
- API key lacks permissions

**Solutions:**
1. Regenerate API key in Dataiku UI
2. Verify key has required permissions
3. Check key is correctly set: `echo $DSS_API_KEY | head -c 10`

## "Project not found"
```
dataikuapi.utils.DataikuException: Project X not found
```

**Causes:**
- Wrong project key
- No access to project
- Project deleted

**Solutions:**
1. List available projects: `client.list_project_keys()`
2. Check project key spelling (case-sensitive)
3. Verify API key has project access
