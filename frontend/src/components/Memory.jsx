// Displays memory

import {useState, useEffect} from 'react';
import {getMemory} from '../api';
import '../App.css';

const Memory = () => {
	const [memory, setMemory] = useState({});

	const fetchMemory = async () => {
		try{
			const response = await getMemory();
			console.log("Fetched Memory", response.data);

			Object.entries(response.data.memory).forEach(([key, value]) => {
				console.log('${key}:', value, "Type: ", typeof value);
			});
			setMemory(response.data.memory || {});
		}
		catch(err){
			alert('Failed to fetch memory', err);
		}
	}

	useEffect(() => {
		fetchMemory();
	}
	, []);

	return (
		<div className="memory-container">
			<h3>Memory</h3>
			<div className="memory-table-container">
			<table class="memory-table">
				<thead>
					<tr>
						<th>Address</th>
						<th>Value</th>
					</tr>
				</thead>
				<tbody>
					{Object.entries(memory).map(([address, value]) => (
						<tr key={address}>
							<td>{address}</td>
							<td>{value}</td>
						</tr>
					))}
				</tbody>
			</table>
			</div>
		</div>
	)

};

export default Memory;