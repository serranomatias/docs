# Mintlify Starter Kit

Click on `Use this template` to copy the Mintlify starter kit. The starter kit contains examples including

- Guide pages
- Navigation
- Customizations
- API Reference pages
- Use of popular components

### Development

Install the [Mintlify CLI](https://www.npmjs.com/package/mintlify) to preview the documentation changes locally. To install, use the following command

```
npm i -g mintlify
```

Run the following command at the root of your documentation (where mint.json is)

```
mintlify dev
```

### Publishing Changes

Install our Github App to auto propagate changes from your repo to your deployment. Changes will be deployed to production automatically after pushing to the default branch. Find the link to install on your dashboard. 

#### Troubleshooting

- Mintlify dev isn't running - Run `mintlify install` it'll re-install dependencies.
- Page loads as a 404 - Make sure you are running in a folder with `mint.json`


Frames :
<!-- <Frame>
  <div style={{ border: '1px solid #ccc', padding: '20px', borderRadius: '8px', textAlign: 'center', position: 'relative' }}>
    <h3>New Feature</h3>
    <p>This exciting new feature will be available soon!</p>
    <span style={{ background: '#ffcc00', color: '#fff', padding: '5px 10px', borderRadius: '5px', position: 'absolute', top: '10px', right: '10px' }}>Coming Soon</span>
    <img src="/images/agents/coming_soon.png" alt="Coming Soon" style={{ width: '100%', marginTop: '20px' }} />
  </div>
</Frame>
<Frame>
  <div style={{ border: '1px solid #ccc', padding: '20px', borderRadius: '8px', textAlign: 'center' }}>
    <h3>New Feature</h3>
    <p>We are working hard to bring you this new feature. Stay tuned!</p>
    <div style={{ background: '#f3f3f3', borderRadius: '5px', overflow: 'hidden', marginTop: '20px' }}>
      <div style={{ width: '60%', background: '#4caf50', padding: '10px 0', color: '#fff', textAlign: 'center' }}>60% Complete</div>
    </div>
  </div>
</Frame>
<Frame>
  <div style={{ border: '1px solid #ccc', padding: '20px', borderRadius: '8px', textAlign: 'center' }}>
    <h3>New Feature</h3>
    <p>Coming in:</p>
    <div style={{ fontSize: '2em', marginTop: '20px' }}>
      <span id="days">10</span> days
    </div>
  </div>
</Frame>


<Frame>
  <div style={{ position: 'relative', textAlign: 'center' }}>
    <img src="/images/agents/new_feature_preview.png" alt="New Feature Preview" style={{ width: '100%', borderRadius: '8px' }} />
    <div style={{ position: 'absolute', top: '0', left: '0', width: '100%', height: '100%', background: 'rgba(0, 0, 0, 0.5)', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '8px' }}>
      <h2>Coming Soon</h2>
    </div>
  </div>
</Frame> -->