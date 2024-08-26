"use client"
import React from 'react';
import { useRouter } from 'next/navigation';
import { Layout, Menu, Breadcrumb, Row, Col,Card,Progress, Statistic } from 'antd';
import { PieChartOutlined, UserOutlined, DesktopOutlined, LogoutOutlined, ArrowUpOutlined,ArrowDownOutlined } from '@ant-design/icons';
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';
import './Dashboard.css'; // Import the CSS file

const { Header, Content, Footer, Sider } = Layout;
const { SubMenu } = Menu;
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
        <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline">
          <Menu.Item key="1" icon={<PieChartOutlined />}>
            Dashboard
          </Menu.Item>
          <Menu.Item key="2" icon={<DesktopOutlined />}>
            Reports
          </Menu.Item>
          <SubMenu key="sub1" icon={<UserOutlined />} title="User Management">
            <Menu.Item key="3" onClick={() => router.push('/addusers')}>Add Employess</Menu.Item>
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
          <Row gutter={[16,16]}>
            <Col xs={24} md={12}>
            <Card title="Statistics" style={{ width: 450, border:"solid black 1px",background:"#EBEBEA", textAlign:"center" }}>
            <Progress type="circle" percent={75} format={percent => `${percent} %`} />
  </Card>
            </Col>
            <Col xs={24} md={12}>
            <Card title="Analytics" style={{ width: 450, border:"solid black 1px",background:"#EBEBEA" }}>

  </Card>
            </Col>
   
          </Row>
          <Row gutter={[16,16]} style={{marginTop:"5rem"}}>
          <Col xs={24} md={12}>
          <Card title="Charts" style={{ width: 450, border:"solid black 1px",background:"#EBEBEA" }}>
          {/* <PieChart width={400} height={400}>
                  <Pie data={data} dataKey="value" nameKey="name" outerRadius={150} fill="#8884d8" label>
                    {data.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={['#0088FE', '#00C49F', '#FFBB28', '#FF8042'][index]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
     */}
  </Card>
            </Col>
            <Col xs={24} md={12}>
            <Card title="Data" style={{ width: 450, border:"solid black 1px",background:"#EBEBEA" }}>
              <Row>
                <Col>
                <Statistic
          title="Active"
          value={11.28}
          precision={2}
          valueStyle={{
            color: '#3f8600',
          }}
          prefix={<ArrowUpOutlined />}
          suffix="%"
        />
                </Col>
                <Col>
                
        <Statistic
          title="Idle"
          value={9.3}
          precision={2}
          valueStyle={{
            color: '#cf1322',
          }}
          prefix={<ArrowDownOutlined />}
          suffix="%"
        />
                </Col>
              </Row>
            
  </Card>
            </Col>
          </Row>
        </Content>
        <Footer style={{ textAlign: 'center', background: '#fff' }}>
        Pharmaregtech ©2024 All Rights Reserved
        </Footer>
      </Layout>
    </Layout>
  );
};

export default Dashboard;
