### AppManager.js - Core Frontend Framework

本文档为AI生成，仅供参考，详细的需要看具体代码逻辑。

**AppManager.js** is a custom-built JavaScript framework that provides a comprehensive solution for building interactive web applications. It serves as the backbone of the frontend architecture.

#### 🏗️ Architecture Overview

**Core Classes:**
- **AppManager**: Main application controller and lifecycle manager
- **AppElement**: Base class for all UI components
- **DialogManager**: Modal dialogs and user interactions
- **FormManager**: Form data handling and validation
- **NetManager**: HTTP requests and API communication
- **Timer**: Time-based utilities and countdowns

#### 🎯 Key Features

**1. Component-Based Architecture**
```javascript
// Register custom components
AppManager.registerElement('data-table', DataTableComponent);
AppManager.registerAction('save', saveFunction);

// Use in HTML
<data-table class="app_element" data-init-data="data:list"></data-table>
```

**2. Event-Driven Communication**
```javascript
// Bind events
app.event('data-changed', function(e, data) {
    console.log('Data updated:', data);
});

// Trigger events
app.trigger('data-changed', newData);
```

**3. Template Engine Integration**
```javascript
// Load templates
app.loadTemplate(['data-form', 'data-search']);

// Render templates
const html = app.template('data-form', formData);
```

**4. Automatic Token Management**
```javascript
// Automatic token handling for API requests
app.setUserToken(token);
const response = await app.post('/api/data', data);
```

**5. Modal Dialog System**
```javascript
// Confirmation dialogs
const confirmed = await app.modal({
    title: 'Confirm Delete',
    content: 'Are you sure?',
    confirmText: 'Delete',
    cancelText: 'Cancel'
});
```

#### 🔧 Technical Implementation

**Component Registration System:**
- Dynamic component loading and registration
- Lifecycle management (init, scan, render)
- Data binding and state management

**Event System:**
- Custom event bus implementation
- Event delegation for dynamic content
- Promise-based async operations

**Template Engine:**
- Art-template integration
- Dynamic template loading
- Data-driven rendering

**API Integration:**
- Automatic authentication headers
- Request/response interceptors
- Error handling and retry logic

#### 📋 Usage Examples

**1. Basic App Initialization:**
```javascript
const app = new AppManager(document.body, {
    host: 'http://localhost:5070',
    netHost: 'http://localhost:5070',
    path: { tpl: '/assets/template/' },
    templateNames: ['data-form', 'data-search']
});

app.start().then(() => {
    console.log('App initialized');
});
```

**2. Custom Component:**
```javascript
class DataTableComponent extends AppElement {
    init() {
        this.loadData();
        this.bindEvents();
    }
    
    async loadData() {
        const data = await this.app.get('/api/dataset/list');
        this.render(data);
    }
}

AppManager.registerElement('data-table', DataTableComponent);
```

**3. Form Handling:**
```javascript
// Get form data
const formData = AppManager.getFormData('#myForm', true, true);

// Set form data
AppManager.setFormData('#myForm', userData, false);
```