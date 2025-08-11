const express = require('express');
const axios = require('axios');
const basicAuth = require('express-basic-auth');
const app = express();

app.use(express.static('public'));
app.use(express.json());

// Basic authentication
app.use(basicAuth({
    users: { [process.env.BASIC_AUTH_USERNAME]: process.env.BASIC_AUTH_PASSWORD },
    challenge: true
}));

// Proxy to Docker API
app.use('/docker-api', async (req, res) => {
    try {
        const response = await axios({
            method: req.method,
            url: `http://localhost:5000${req.url.replace('/docker-api', '')}`,
            data: req.body
        });
        res.status(response.status).json(response.data);
    } catch (error) {
        res.status(error.response?.status || 500).json({
            error: error.message
        });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Web VPS interface running on port ${PORT}`);
});
