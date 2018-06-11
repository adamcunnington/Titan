import React from 'react';
import AcquireItem from './acquire-item.jsx';

require('./acquire-list.css');

class AcquireList extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      acquires: this.props.acquires
    };

    this.add = this.add.bind(this);
    this.remove = this.remove.bind(this);
    this.itemChange = this.itemChange.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.acquires !== this.state.acquires) {
      this.setState({
        acquires: nextProps.acquires
      });
    } 
  }

  // Add another acquire to list
  add() {

    const acquires = this.state.acquires;

    const newAcquire = {
      ScheduledAcquireName: name,
      Options: this.props.optionNames.map(name => {
        return {
          ScheduledAcquireOptionName: name,
          ScheduledAcquireOptionValue: ''
        }
      })
    };

    acquires.push(newAcquire);

    this.setState({
      acquires: acquires
    });

    this.props.onChange(acquires);
  }

  remove(index) {

    let acquires = this.state.acquires;
    acquires.splice(index, 1);
    this.setState({
      acquires: acquires
    });

    this.props.onChange(acquires);
  }

  itemChange(index, name, value) {
    const acquires = this.state.acquires;
    acquires[index].Options
      .find(option => option.ScheduledAcquireOptionName === name).ScheduledAcquireOptionValue = value;

    this.setState({
      acquires: acquires
    });

    this.props.onChange(acquires);
  }

  render() {

    const acquireItems = this.state.acquires.map((acquire, index) => {
      return <AcquireItem key={index} acquire={acquire}
        index={index} remove={this.remove} onChange={this.itemChange} />
    });

    return (
      <div className="acquire-list">
        { acquireItems }
        { !this.state.acquires.length && <p>No acquires</p> }
        <a onClick={this.add}>+ Add another</a>
      </div>
    );
  }
}

export default AcquireList;
  