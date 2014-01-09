our-will
========

Our @will, the friendliest bot anywhere.  He's a greenkahuna [will](https://github.com/greenkahuna/will) bot.


### What's included
Our will includes a bunch of greenkahuna-specific plugins, and stuff we find fun but everyone might not.  

For fun, it's things like:

- walkmaster
- gold stars
- hello / goodbye / g'night
- daily standups
- IE8 warnings

For biz, it's things lik:

- our code flow tool (CR/FR/CD)
- provisioning and deployment of staging servers
- uptime
- AWS dev bucket cleanup


### Buildpacks.
Since we need the heroku gem, we do need a custom buildpack on heroku. We use [heroku-buildpack-multi](https://github.com/ddollar/heroku-buildpack-multi)
```
heroku config:add BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git
```


### Environment
We've got some custom environment variables you'll need to get running. If you're a greenkahuna developer, don't worry - it's all taken care of by boxen.

```
export WILL_GITHUB_USERNAME=''
export WILL_GITHUB_PASSWORD=''
export WILL_GITHUB_ORGANIZATION_NAME=''
export WILL_HEROKU_API_KEY=''

export GOLD_STAR_URL=''
export WILL_AWS_ACCESS_KEY_ID=''
export WILL_AWS_SECRET_ACCESS_KEY=''
export WILL_AWS_DEV_BUCKET_NAME=''
```