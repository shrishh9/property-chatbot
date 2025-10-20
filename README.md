# 🏠 Property Search Chatbot

An intelligent property search chatbot that uses natural language processing to help users find properties based on their requirements. Built with Flask backend API and Next.js frontend interface.

## 🌟 Features

- 🤖 **Natural Language Query Understanding** - Ask questions in plain English
- 🔍 **Smart Property Filtering** - Filter by BHK, price, location, and status
- 💬 **ChatGPT-style Interface** - Modern conversational UI
- 📊 **Real-time Search Results** - Instant property cards display
- 🎨 **Responsive Design** - Works on desktop and mobile
- 🏷️ **Intelligent Greeting Handling** - Friendly bot interactions
- 📈 **83+ Properties Database** - CSV-based property data

## 🚀 Live Demo

- **Frontend:** [[https://your-app.netlify.app](https://68f62bc760a0a000085cb45f--velvety-alpaca-ef6033.netlify.app/)]
- **Backend API:** [[https://property-chatbot-w9rn.onrender.com](https://property-chatbot-w9rn.onrender.com/)]
- **JSON data with properties:**[https://property-chatbot-w9rn.onrender.com/api/properties
- **Health Check**https://property-chatbot-w9rn.onrender.com/api/health

### Example Queries
- "hi" - Get greeted and see usage examples
- "3BHK in Pune under 1.2 Cr" - Search by BHK, location, and price
- "Ready to move 2BHK" - Filter by status and BHK
- "Office space in Mumbai" - Search commercial properties
- "Show me all properties" - Browse all available listings

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 15 (React 19)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Icons**: Lucide React

### Backend
- **Framework**: Flask (Python)
- **Data Processing**: Pandas, NumPy
- **Web Server**: Gunicorn
- **CORS**: Flask-CORS

### Deployment
- **Frontend**: Netlify / Vercel
- **Backend**: Render
- **Version Control**: GitHub
- ## 🚀 Getting Started

### Prerequisites

- **Node.js** 18+ ([Download](https://nodejs.org/))
- **Python** 3.11+ ([Download](https://www.python.org/))
- **npm**
- **Git** ([Download](https://git-scm.com/))

### Installation

#### 1. Clone the Repository
git clone https://github.com/shrishh9/property-chatbot.git
cd property-chatbot

#### 2. Backend Setup

Navigate to backend folder
cd backend

Create virtual environment
python -m venv venv

Activate virtual environment
Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

Install dependencies
pip install -r requirements.txt

Run the server
python app.py

text

Backend will run on: [**http://localhost:5000**](http://localhost:5000)

#### 3. Frontend Setup

Navigate to frontend folder (open new terminal)
cd frontend

Install dependencies
npm install

Run development server
npm run dev

Frontend will run on: [**http://localhost:3000**](http://localhost:3000)

### Environment Variables

#### Frontend (.env.local)

Create `frontend/.env.local`:

NEXT_PUBLIC_API_URL=http://localhost:5000/api

For production:
NEXT_PUBLIC_API_URL=https://property-chatbot-w9rn.onrender.com/api

#### Backend (.env) - Optional

FLASK_ENV=development
PORT=5000

## 📊 Data Structure

The chatbot works with CSV files containing property data:

- **project.csv**: Main property information
- **ProjectAddress.csv**: Location details
- **ProjectConfiguration.csv**: Property configurations
- **ProjectConfigurationVariant.csv**: BHK variants and pricing
- **merged_properties.csv**: Combined dataset (auto-generated)

## 🔧 API Endpoints

### Health Check
GET /api/health

### Get All Properties
GET /api/properties

## 🎯 Query Parser Features

The NLP engine understands:

- **BHK**: 1BHK, 2BHK, 3BHK, 4BHK, 5BHK
- **Price**: "under 1.2 Cr", "below 50 lakhs", "less than 1 crore"
- **Location**: City names (Pune, Mumbai, etc.)
- **Status**: Ready to move, Under construction
- **Property Type**: Office, Villa, Residential, Commercial

### Example Queries

✅ "3BHK flat in Pune under ₹1.2 Cr"
✅ "Ready to move 2BHK apartments in Mumbai"
✅ "Office space under 50 lakhs"
✅ "Show me all 3BHK properties"
✅ "Properties under construction in Pune"

text

## 🌐 Deployment

### Deploy Backend to Render

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Create new **Web Service**
4. Connect repository
5. Set **Root Directory**: `backend`
6. Set **Build Command**: `pip install -r requirements.txt`
7. Set **Start Command**: `gunicorn app:app`
8. Set Environment Variables:
   - `PYTHON_VERSION=3.11.0`
9. Deploy!

### Deploy Frontend to Vercel/Netlify

#### Netlify
1. Go to [netlify.com](https://www.netlify.com)
2. Import repository
3. Set **Base directory**: `frontend`
4. Set **Build command**: `npm run build`
5. Set **Publish directory**: `frontend/.next`
6. Add Environment Variable:
- `NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com/api`
7. Deploy!

## 🧪 Testing

### Test Backend API
