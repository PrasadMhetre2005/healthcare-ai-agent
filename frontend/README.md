# HealthCare AI - Frontend Dashboard

A modern React application for real-time patient health monitoring with AI-powered insights.

## 🎯 Features

- **User Authentication** - Secure login/registration system
- **Patient Dashboard** - Real-time health metrics display
- **Health Data Logging** - Easy input of vital signs and lab results
- **Alert Management** - Active and resolved health alerts
- **AI Insights** - GPT-powered health analysis and recommendations
- **Responsive Design** - Works on desktop, tablet, and mobile

## 🛠️ Tech Stack

- **React 18** - UI library
- **React Router 6** - Navigation
- **Axios** - API client
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Vite** - Build tool
- **Lucide React** - Icons

## ⚙️ Setup Instructions

### 1. Prerequisites
- Node.js 16+ (LTS recommended)
- npm or yarn

### 2. Install Dependencies

```bash
cd frontend
npm install
```

### 3. Environment Configuration

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

### 4. Start Development Server

```bash
npm run dev
```

The app will open at `http://localhost:3000`

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/           # Reusable React components
│   │   ├── Sidebar.jsx       # Navigation sidebar
│   │   ├── Header.jsx        # Page headers
│   │   ├── Alert.jsx         # Alert component
│   │   ├── MetricCard.jsx    # Health metric display
│   │   ├── Charts.jsx        # Chart components
│   │   └── PrivateRoute.jsx  # Protected routes
│   │
│   ├── pages/                # Full page components
│   │   ├── LoginPage.jsx     # User login
│   │   ├── RegisterPage.jsx  # User registration
│   │   ├── DashboardPage.jsx # Main dashboard
│   │   ├── HealthDataPage.jsx# Health data logging
│   │   ├── AlertsPage.jsx    # Alerts management
│   │   └── InsightsPage.jsx  # AI insights
│   │
│   ├── services/             # API integration
│   │   └── api.js            # Axios instance & API calls
│   │
│   ├── context/              # React context
│   │   └── AuthContext.js    # Authentication state
│   │
│   ├── hooks/                # Custom hooks
│   │   └── useAuth.js        # Auth hook
│   │
│   ├── styles/               # Global styles
│   │   └── index.css         # Tailwind + custom CSS
│   │
│   ├── App.jsx               # Main app component
│   └── main.jsx              # React entry point
│
├── public/                   # Static assets
├── package.json              # Dependencies
├── vite.config.js           # Vite configuration
├── tailwind.config.js       # Tailwind configuration
└── README.md                # This file
```

## 🔌 API Integration

The frontend connects to the backend at `http://localhost:8000`

### Authentication

- Register: `POST /api/auth/register`
- Login: `POST /api/auth/login`

### Protected Routes

All requests include JWT token in Authorization header:
```
Authorization: Bearer {token}
```

## 🛣️ Application Routes

| Route | Component | Purpose |
|-------|-----------|---------|
| `/login` | LoginPage | User login |
| `/register` | RegisterPage | User registration |
| `/dashboard` | DashboardPage | Main health dashboard |
| `/health-data` | HealthDataPage | Log health metrics |
| `/alerts` | AlertsPage | Manage health alerts |
| `/insights` | InsightsPage | View AI insights & recommendations |

## 🎨 UI Components

### Sidebar
- User profile info
- Navigation menu
- Logout button

### Header
- Page title
- Subtitle/description

### MetricCard
- Health metric display
- Status indicator (normal/warning/critical)
- Trend indicator

### Charts
- Line graphs for trends
- Bar charts for comparisons
- Responsive design

### Alert
- Alert type (info/warning/danger/success)
- Title and message
- Close button

## 🔐 Authentication Flow

```
1. User visits /login or /register
2. Validates credentials/registration
3. Backend returns JWT token
4. Token stored in localStorage
5. Token included in all API requests
6. Protected routes check authentication
7. Automatic logout on token expiration
```

## 🚀 Build for Production

```bash
npm run build
```

Creates optimized build in `dist/` directory

## 📦 Deployment

### Option 1: Static Hosting (Vercel, Netlify)

```bash
npm run build
# Deploy 'dist' folder to platform
```

### Option 2: Docker

```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .

RUN npm run build

FROM node:18-alpine
RUN npm install -g serve
WORKDIR /app
COPY --from=0 /app/dist ./dist

EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
```

### Option 3: Express Server

Create `server.js`:

```javascript
const express = require('express');
const path = require('path');

const app = express();
app.use(express.static(path.join(__dirname, 'dist')));

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000
lsof -i :3000
kill -9 <PID>
```

### API Connection Error
- Ensure backend is running on `http://localhost:8000`
- Check VITE_API_URL environment variable
- Verify CORS is enabled on backend

### Login Issues
- Verify user credentials
- Check token is stored in localStorage
- Ensure JWT_SECRET matches backend

### Charts Not Displaying
- Verify health data exists in backend
- Check console for JavaScript errors
- Ensure Recharts is installed

## 📝 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | `http://localhost:8000` | Backend API URL |
| `VITE_APP_NAME` | `HealthCare AI` | App name |

## 🎓 Development Tips

### Code Formatting
```bash
npm run format
```

### Linting
```bash
npm run lint
```

### Debug Mode
Add `debugger;` in React components or use Chrome DevTools

## 📊 Performance

- **Code splitting** - Routes use lazy loading
- **Image optimization** - Icons from Lucide (SVG)
- **CSS efficiency** - Tailwind with PurgeCSS
- **Bundle size** - ~200KB gzipped

## 🔄 State Management

- **AuthContext** - User authentication state
- **Local Storage** - Persistent session
- **React Hooks** - Component-level state

## 🤝 API Response Format

### Successful Response
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "role": "patient"
}
```

### Error Response
```json
{
  "detail": "Invalid credentials"
}
```

## 📱 Mobile Responsiveness

- Sidebar collapses on mobile
- Grid layouts adapt to screen size
- Touch-friendly buttons
- Scrollable on small screens

## 🔗 Related Documentation

- [Backend API Documentation](../backend/API.md)
- [Backend Architecture](../backend/ARCHITECTURE.md)
- [Backend Setup Guide](../backend/README.md)

## 🆘 Support

For issues or questions:
1. Check error messages in console
2. Review API documentation
3. Verify backend is running
4. Check network tab in DevTools

## 📄 License

MIT License - See LICENSE file

## 👥 Team

Built for the Healthcare AI Hackathon - April 2026

---

**Ready to run?** → `npm install && npm run dev`
