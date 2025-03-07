const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();

// Middleware
app.use(cors());
app.use(express.json({ limit: '50mb' }));

// MongoDB Connection
mongoose.connect('mongodb://localhost:27017/gardenPlanner', {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => {
    console.log('Connected to MongoDB');
}).catch((err) => {
    console.error('MongoDB connection error:', err);
});

// Define Schemas
const DrawingSchema = new mongoose.Schema({
    imageData: String,
    createdAt: { type: Date, default: Date.now }
});

const LocationDataSchema = new mongoose.Schema({
    climate: String,
    direction: String,
    temperature: String,
    location: String,
    createdAt: { type: Date, default: Date.now }
});

const PlantSelectionSchema = new mongoose.Schema({
    vegetables: [{ name: String, id: String }],
    fruits: [{ name: String, id: String }],
    herbs: [{ name: String, id: String }],
    flowers: [{ name: String, id: String }],
    createdAt: { type: Date, default: Date.now }
});

// Create Models
const Drawing = mongoose.model('Drawing', DrawingSchema);
const LocationData = mongoose.model('LocationData', LocationDataSchema);
const PlantSelection = mongoose.model('PlantSelection', PlantSelectionSchema);

// API Routes
// Save drawing
app.post('/api/drawings', async (req, res) => {
    try {
        const drawing = new Drawing({
            imageData: req.body.imageData
        });
        await drawing.save();
        res.json({ success: true, id: drawing._id });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Save location data
app.post('/api/location', async (req, res) => {
    try {
        const locationData = new LocationData(req.body);
        await locationData.save();
        res.json({ success: true, id: locationData._id });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Save plant selections
app.post('/api/plants', async (req, res) => {
    try {
        const plantSelection = new PlantSelection(req.body);
        await plantSelection.save();
        res.json({ success: true, id: plantSelection._id });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Get latest data
app.get('/api/garden-data', async (req, res) => {
    try {
        const drawing = await Drawing.findOne().sort({ createdAt: -1 });
        const location = await LocationData.findOne().sort({ createdAt: -1 });
        const plants = await PlantSelection.findOne().sort({ createdAt: -1 });
        
        res.json({
            drawing,
            location,
            plants
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Start server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});