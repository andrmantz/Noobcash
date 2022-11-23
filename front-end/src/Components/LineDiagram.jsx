import React from 'react'
import { AreaChart , Area, ResponsiveContainer, XAxis, YAxis, Tooltip } from 'recharts';

const LineDiagram = ({ data }) => {

    return (
        <ResponsiveContainer width={"99%"} aspect={1} maxHeight={200}>
            <AreaChart margin={{ top: 5, right: 5, bottom: 5, left: 5 }} data={data?.map(({ index, amount }) => ({ index, amount }))}>
                {/* <Line type="monotone" dataKey="cart_tuples" stroke="#8884d8" /> */}
                <defs>
                    <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
                    </linearGradient>
                    {/* <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#82ca9d" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#82ca9d" stopOpacity={0}/>
                    </linearGradient> */}
                </defs>
                <XAxis dataKey="index" />
                <YAxis />
                <Area type="monotone" dataKey="amount" stroke="#8884d8" fillOpacity={1} fill="url(#colorUv)" />
            </AreaChart>
        </ResponsiveContainer>
    )
}

export default LineDiagram;