import { useState } from 'react';
import { Outlet } from 'react-router-dom';

import Sidebar from '../components/layout/Sidebar';
import Navbar from '../components/layout/Navbar';

import '../styles/layout.css';

export default function MainLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="layout">
      <Sidebar sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

      <div className="layout-main">
        <Navbar sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

        <main className="layout-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
