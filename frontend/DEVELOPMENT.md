# HealthCare AI Frontend - Development Guide

## Quick Navigation

- **Getting Started** → Install dependencies & run dev server
- **Project Structure** → Understanding the codebase
- **Component Library** → Available components
- **API Integration** → Backend communication
- **Deployment** → Production builds

---

## Getting Started

### 1. Install & Run

```bash
cd frontend
npm install
npm run dev
```

⚠️ **Make sure the backend is running first!** (http://localhost:8000)

Visit http://localhost:3000

### 2. Test User

For development, create a test account:
- Username: `testuser`
- Email: `test@example.com`
- Password: `password123`
- Role: `patient`

---

## Pages Overview

### 🔐 **LoginPage** (`/login`)
- User authentication
- Form validation
- Error handling
- Link to registration

### 📝 **RegisterPage** (`/register`)
- New account creation
- Dual-role support (patient/doctor)
- Password confirmation
- Email validation

### 📊 **DashboardPage** (`/dashboard`)
- Welcome summary
- Latest health metrics
- Active alerts
- Quick action buttons

### 📈 **HealthDataPage** (`/health-data`)
- Health metric form (BP, HR, etc.)
- Real-time chart visualization
- Data history
- Trend analysis

### ⚠️ **AlertsPage** (`/alerts`)
- Active health alerts
- Alert severity levels
- Resolved alerts archive
- Alert dismissal

### 💡 **InsightsPage** (`/insights`)
- AI-generated health insights
- Personalized recommendations
- Recommendation categories
- Generate new recommendations

---

## Components Breakdown

### Sidebar
```jsx
// Shows user info and navigation
- User profile section
- Navigation links
- Logout button
```

### MetricCard
```jsx
// Displays single health metric
<MetricCard
  title="Blood Pressure"
  value="130/85"
  unit="mmHg"
  status="warning"
  icon={Heart}
/>
```

### Charts
```jsx
// Recharts integration
<LineGraph
  data={healthData}
  dataKey="heart_rate"
  title="Heart Rate Trend"
/>
```

### Alert
```jsx
// Alert notifications
<Alert
  type="danger"
  title="Alert Title"
  message="Alert message text"
  onClose={() => {}}
/>
```

---

## API Calls

### Example: Logging Health Data

```javascript
import { healthDataService } from '../services/api';

const logHealth = async () => {
  try {
    const data = await healthDataService.logHealthData({
      blood_pressure_systolic: 130,
      blood_pressure_diastolic: 85,
      heart_rate: 72,
      // ... more fields
    });
    console.log('Logged:', data);
  } catch (error) {
    console.error('Error:', error);
  }
};
```

### Example: Getting Alerts

```javascript
import { alertService } from '../services/api';

const getAlerts = async () => {
  const alerts = await alertService.getUnresolved(patientId);
  setAlerts(alerts);
};
```

---

## State Management

### Authentication Context

```javascript
import { useAuth } from './hooks/useAuth';

const { user, token, login, logout, isAuthenticated } = useAuth();
```

### Local Component State

```javascript
const [loading, setLoading] = useState(false);
const [data, setData] = useState(null);
const [error, setError] = useState('');
```

---

## Styling

### Tailwind Classes

```jsx
// Card component
<div className="card">
  <h2 className="card-header">Title</h2>
</div>

// Buttons
<button className="btn-primary">Primary</button>
<button className="btn-secondary">Secondary</button>
<button className="btn-danger">Danger</button>

// Badges
<span className="badge-success">Success</span>
<span className="badge-warning">Warning</span>
<span className="badge-danger">Danger</span>
```

### Custom CSS

Located in `src/styles/index.css`:
- Component classes (`.card`, `.btn`, etc.)
- Typography
- Animations
- Responsive utilities

---

## Common Tasks

### Add a New Page

1. Create file in `src/pages/NewPage.jsx`
2. Import components needed
3. Add route in `App.jsx`
4. Add navigation link in Sidebar

### Add a New Component

1. Create file in `src/components/NewComponent.jsx`
2. Export as named export
3. Import in pages
4. Pass required props

### API Call

1. Add method to `src/services/api.js`
2. Call from component with try/catch
3. Handle loading/error states
4. Show toast notifications

---

## Error Handling

All API errors are intercepted:

```javascript
// Auto-logout on 401
// Error toast notifications
// Fallback error messages
```

---

## Testing

### Manual Testing Checklist

- [ ] Login with invalid credentials
- [ ] Register with duplicate email
- [ ] Log health data with various inputs
- [ ] Create alert conditions
- [ ] Generate recommendations
- [ ] Resolve alerts
- [ ] Browser back/forward navigation
- [ ] Mobile responsiveness

---

## Performance Tips

- **Code Splitting** - Routes lazy load
- **Image Optimization** - SVG icons
- **CSS Purging** - Unused styles removed
- **API Caching** - Consider implementing

---

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

## Debugging

### Chrome DevTools

1. Open DevTools (F12)
2. Check Console for errors
3. Network tab to see API calls
4. Application tab for localStorage

### React DevTools Extension

- Component tree inspection
- Props checking
- State debugging

---

## Environment Setup

### .env File

```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=HealthCare AI
```

### Running Different Environments

```bash
# Development
npm run dev

# Production build
npm run build

# Preview production
npm run preview
```

---

## Next Steps

1. ✅ Frontend dashboard complete
2. ⏭️ Add patient profile management
3. ⏭️ Add doctor dashboard
4. ⏭️ Implement WebSocket for real-time updates
5. ⏭️ Add data export/reporting

---

**Questions?** Check the README.md for more details!
