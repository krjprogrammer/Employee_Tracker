"use client"
import React from 'react';
import { useRouter } from 'next/navigation';
import { Layout, Menu, Breadcrumb, Row, Col,Card,Progress, Statistic,message, Upload  } from 'antd';
import { PieChartOutlined, UserOutlined, DesktopOutlined, LogoutOutlined, ArrowUpOutlined,ArrowDownOutlined,InboxOutlined  } from '@ant-design/icons';
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';
import './Dashboard.css'; // Import the CSS file
const { Dragger } = Upload
const { Header, Content, Footer, Sider } = Layout;
const { SubMenu } = Menu;
const props = {
    name: 'file',
    multiple: true,
    action: 'http://127.0.0.1:4000/upload_employee_data',
    onChange(info) {
      const { status } = info.file;
      if (status !== 'uploading') {
        console.log(info.file, info.fileList);
      }
      if (status === 'done') {
        message.success(`${info.file.name} file uploaded successfully.`);
      } else if (status === 'error') {
        message.error(`${info.file.name} file upload failed.`);
      }
    },
    onDrop(e) {
      console.log('Dropped files', e.dataTransfer.files);
    },
  };
const data = [
  { name: 'Group A', value: 400 },
  { name: 'Group B', value: 300 },
  { name: 'Group C', value: 300 },
  { name: 'Group D', value: 200 },
];

const userData = [
  { key: '1', name: 'John Doe', email: 'john.doe@example.com', role: 'Admin' },
  { key: '2', name: 'Jane Smith', email: 'jane.smith@example.com', role: 'User' },
  { key: '3', name: 'Tom Brown', email: 'tom.brown@example.com', role: 'User' },
  { key: '4', name: 'Emily Johnson', email: 'emily.johnson@example.com', role: 'User' },
];

const columns = [
  { title: 'Name', dataIndex: 'name', key: 'name' },
  { title: 'Email', dataIndex: 'email', key: 'email' },
  { title: 'Role', dataIndex: 'role', key: 'role' },
];

const Dashboard = () => {
  const router = useRouter(); // Moved inside the component

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider width={256} className="site-layout-background">
        <div className="logo">
          <h3>Pharmaregtech</h3>
        </div>
        <Menu theme="dark" mode="inline">
          <Menu.Item key="1" icon={<PieChartOutlined onClick={() => router.push('/home')}/>}>
            Dashboard
          </Menu.Item>
          <Menu.Item key="2" icon={<DesktopOutlined />}>
            Reports
          </Menu.Item>
          <SubMenu key="sub1" icon={<UserOutlined />} title="User Management">
            <Menu.Item key="3" >Add Employees</Menu.Item>
            <Menu.Item key="4">View Employees</Menu.Item>
          </SubMenu>
          <Menu.Item key="5" icon={<LogoutOutlined/>} onClick={() => router.push('/')}>
            Logout
          </Menu.Item>
        </Menu>
      </Sider>
      <Layout style={{ flex: 1 }}>
        <Header className="site-layout-background" style={{ padding: 0, background: '#fff' }} />
        <Content style={{ margin: '0 16px', padding:"0 48px" }}>
          <Breadcrumb style={{ margin: '16px 0' }}>
            <Breadcrumb.Item>Dashboard</Breadcrumb.Item>
            <Breadcrumb.Item>Overview</Breadcrumb.Item>
          </Breadcrumb>
          <Dragger {...props} height={400} style={{border:"solid black 1px"}}>
    <p className="ant-upload-drag-icon">
      <InboxOutlined />
    </p>
    <p className="ant-upload-text">Click or drag file to this area to upload</p>
    <p className="ant-upload-hint">
      Support for a single or bulk upload. Strictly prohibited from uploading company data or other
      banned files.
    </p>
  </Dragger>

        </Content>
        <Footer style={{ textAlign: 'center', background: '#fff' }}>
          Pharmaregtech ©2024 All Rights Reserved
        </Footer>
      </Layout>
    </Layout>
  );
};

export default Dashboard;
