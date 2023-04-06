 // eslint-disable-next-line
import React, { useState, useEffect, useContext } from "react";
import Select from "react-select"
import LoadingSpin from "react-loading-spin";
import { AgChartsReact } from 'ag-charts-react';
import AuthContext from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'
export default function Analyzer() {
    const history = useNavigate()
    let { server, user, authTokens, logoutUser } = useContext(AuthContext)
    // React state to manage selected options
    const [isLoading, setisLoading] = useState(true)
    // Array of all options
    const [optionListdate, setoptionListdate] = useState([])
    const [selecteddate, setSelecteddate] = useState([]);
    const [optionListstatus, setoptionListstatus] = useState([])
    const [selectedstatus, setSelectedstatus] = useState([]);
    const [optionListtype, setoptionListtype] = useState([])
    const [selectedtype, setSelectedtype] = useState([]);
    const [initialstatus, setInitialstatus] = useState([])
    const [initialtype, setInitialtype] = useState([])
    useEffect(() => {
        return () => {
            if (!user) {
                history('/login')
            }
            else {
                const temp = [];
                fetch(`${server}/init/date`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + String(authTokens.access)
                    }
                })
                    .then((response) => {
                        if(response.statusText === 'Unauthorized'){
                            logoutUser()
                        }
                        return response.json()
                    }).then(tdata => {
                        const data = tdata["list"]
                        data.map((i, num) => (
                            temp.push({
                                value: i,
                                label: i,
                            })
                        ))
                        setoptionListdate(temp);
                        setisLoading(false);
                    })
                    .catch((err) => {
                        console.log(err)
                    })

                const temp1 = []
                const temp_series = []
                fetch(`${server}/init/status_code`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + String(authTokens.access)
                    }
                })
                    .then((response) => {
                        if(response.statusText === 'Unauthorized'){
                            logoutUser()
                        }
                        return response.json()
                    }).then(tdata => {
                        const data = tdata["list"]
                        data.map((i, num) => (
                            temp1.push({
                                value: i,
                                label: i.toString(),
                            }), // eslint-disable-line
                            temp_series.push({
                                type: 'column',
                                xKey: 'date',
                                yKey: i,
                                yName: i.toString(),
                                stacked: true,
                            })
                        ))
                        setInitialstatus(temp_series)
                        setOptionsstatus(prev => ({ ...prev, series: temp_series }))
                        setoptionListstatus(temp1);
                        setisLoading(false);
                    })
                    .catch((err) => {
                        console.log(err)
                    })

                const temp2 = [];
                const temp_type = []
                fetch(`${server}/init/type`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + String(authTokens.access)
                    }
                })
                    .then((response) => {
                        if(response.statusText === 'Unauthorized'){
                            logoutUser()
                        }
                        return response.json()
                    }).then(tdata => {
                        const data = tdata["list"]
                        data.map((i, num) => (
                            temp2.push({
                                value: i,
                                label: i,
                            }), // eslint-disable-line
                            temp_type.push({
                                type: 'column',
                                xKey: 'date',
                                yKey: i,
                                yName: i,
                                stacked: true,
                            })
                        ))
                        setInitialtype(temp_type)
                        setOptionstype(prev => ({ ...prev, series: temp_type }))
                        setoptionListtype(temp2);
                        setisLoading(false);
                    })
                    .catch((err) => {
                        console.log(err)
                    })

                const temp3 = []
                const temp_status_data = []
                const temp_type_data = []
                fetch(`${server}/init`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + String(authTokens.access)
                    }
                })
                    .then((response) => {
                        if(response.statusText === 'Unauthorized'){
                            logoutUser()
                        }
                        return response.json()
                    }).then(tdata => {
                        const data = tdata["list"]
                        data.map((i, num) => (
                            
                            temp3.push({
                                date: i["date"],
                                total_logs: i["total_logs"],
                            }), // eslint-disable-line
                           
                            temp_status_data.push({ ...i["status_code"], date: i["date"] }), // eslint-disable-line
                            
                            temp_type_data.push({ ...i["type"], date: i["date"] }) 


                        ))
                        setOptionstotal(prev => ({ ...prev, data: temp3 }))
                        setOptionsstatus(prev => ({ ...prev, data: temp_status_data }))
                        setOptionstype(prev => ({ ...prev, data: temp_type_data }))
                        setisLoading(false);
                    })
                    .catch((err) => {
                        console.log(err)
                    })

            }
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])
    useEffect(() => {
        const x = [], y = [], z = [], temp_series = [], temp_type = [], temp3 = [], temp_status_data = [], temp_type_data = []
        selecteddate.map((i) => (
            x.push(i["value"])
        ))
        selectedstatus.map((i) => (
            y.push(i["value"]), // eslint-disable-line
            temp_series.push({
                type: 'column',
                xKey: 'date',
                yKey: i["value"],
                yName: i["value"].toString(),
                stacked: true,
            })
        ))
        setOptionsstatus(prev => ({ ...prev, series: temp_series }))
        selectedtype.map((i) => (
            z.push(i["value"]), // eslint-disable-line
            temp_type.push({
                type: 'column',
                xKey: 'date',
                yKey: i["value"],
                yName: i["value"],
                stacked: true,
            })
        ))
        setOptionstype(prev => ({ ...prev, series: temp_type }))
        fetch(`${server}/search`, {
            method: 'post',
            headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + String(authTokens.access) },
            body: JSON.stringify({
                "date": x,
                "status_code": y,
                "type": z
            })
        })
            .then(response => {
                if(response.statusText === 'Unauthorized'){
                    logoutUser()
                }
                return response.json()})
            .then(tdata => {
                const data = tdata["list"]
                console.log(data);
                data.map((i, num) => (
                  
                    temp3.push({
                        date: i["date"],
                        total_logs: i["total_logs"], 
                    }), // eslint-disable-line
              
                    temp_status_data.push({ ...i["status_code"], date: i["date"] }), // eslint-disable-line
                
                    temp_type_data.push({ ...i["type"], date: i["date"] }) 


                )) 
                
    
                setOptionstotal(prev => ({ ...prev, data: temp3 }))
                setOptionsstatus(prev => ({ ...prev, data: temp_status_data }))
                setOptionstype(prev => ({ ...prev, data: temp_type_data }))
                setisLoading(false);
            })
            .catch((error) => {
                console.error(error);
            })
            // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [selectedstatus, selecteddate, selectedtype])

    function handleSelecttype(data) {
        if (data.length === 0) {
            setOptionstype(prev => ({ ...prev, series: initialtype }))
        }
        setSelectedtype(data);



    }
    function handleSelectdate(data) {
        
        setSelecteddate(data);

    }
    function handleSelectstatus(data) {
        if (data.length === 0) {
            setOptionsstatus(prev => ({ ...prev, series: initialstatus }))
        }

        setSelectedstatus(data);


    }
    const [optionstotal, setOptionstotal] = useState({
        title: {
            text: "Total count of logs",
        },
        data: [],
        series: [
            {
                type: 'column',
                xKey: 'date',
                yKey: 'total_logs',
                yName: 'Total Logs'
            }
        ]
    });
    const [optionsstatus, setOptionsstatus] = useState({
        title: {
            text: "Logs count by log level (Status Codes)",
        },
        data: [],
        series: [
        ]
    });
    const [optionstype, setOptionstype] = useState({
        title: {
            text: "Logs count by log type (mime-type)",
        },
        data: [],
        series: []
    });
    return (
        <>
            {isLoading && <div><div className="position-absolute top-50 start-50 translate-middle"><LoadingSpin duration="2s"
                width="15px"
                timingFunction="ease-in-out"
                direction="alternate"
                size="200px"
                primaryColor=" #0000FF"
                secondaryColor="grey"
                numberOfRotationsInAnimation={2} /></div></div>}


            {!isLoading && <><nav className="navbar  navbar-dark bg-dark">
                <div className="container-fluid">
                    <a className="navbar-brand" href="/"><h1>Network Log Analyzer</h1></a>
                    <button className="btn btn-danger" onClick={logoutUser} style={{ marginRight: '8px' }}>Logout</button>
                </div>
            </nav>
                <div className="row bg-dark text-light p-3">
                    <h3 className="text-center"> </h3>
                    <div className="col-md-4 col-sm-12 d-flex justify-content-center text-center"><div className="app">

                        <div className="dropdown-container">
                            <div className="">  <h4>Dates</h4>          <Select
                                options={optionListdate}
                                placeholder="Select color"
                                value={selecteddate}
                                onChange={handleSelectdate}
                                isSearchable={true}
                                isMulti
                                className="text-dark"

                            /></div>
                        </div>
                    </div></div>
                    <div className="col-md-4 col-sm-12  d-flex justify-content-center text-center"><div className="app">

                        <div className="dropdown-container">
                            <div className="">   <h4>Status Code</h4>         <Select
                                options={optionListstatus}
                                placeholder="Select color"
                                value={selectedstatus}
                                onChange={handleSelectstatus}
                                isSearchable={true}
                                isMulti
                                className="text-dark"
                            /></div>

                        </div>
                    </div></div>
                    <div className="col-md-4 col-sm-12 d-flex justify-content-center text-center"><div className="app">

                        <div className="dropdown-container">
                            <div className="">   <h4>Meme Type</h4>         <Select
                                options={optionListtype}
                                placeholder="Select color"
                                value={selectedtype}
                                onChange={handleSelecttype}
                                isSearchable={true}
                                isMulti
                                className="text-dark"
                            /></div>
                        </div>
                    </div></div>
                </div>
                <div className="container">  <AgChartsReact options={optionstotal} /><AgChartsReact options={optionsstatus} /><AgChartsReact options={optionstype} /></div></>}
        </>
    )
}
