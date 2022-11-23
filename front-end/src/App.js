import React, { useState } from 'react'
import Account from './Components/Account';
import Actions from './Components/Actions';
import Analytics from './Components/Analytics';
import Dashboard from './Components/Dashboard';
import Login from './Components/Login';
import SideBar from './Components/SideBar'

const App = ({ page }) => {
    const renderPage = () => {
        switch (page) {
            case "analytics":
                return <Analytics />
            case "actions":
                return <Actions />
            case "account":
                return <Account />
            case "login":
                return <Login />
            default:
                return <Dashboard />
        }
    }

    return (
        <SideBar page={page}>
            { renderPage() }
        </SideBar>
    )
}

export default App;