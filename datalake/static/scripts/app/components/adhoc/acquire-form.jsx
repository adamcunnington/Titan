import React from 'react';
import AcquireEntry from './acquire-entry.jsx';

class AcquireForm extends React.Component {

  constructor(props) {
    super(props);
    this.addAnother = this.addAnother.bind(this);
  }

  addAnother() {
    this.props.addAnother();
  }

  render() {

    const acquireEntries = this.props.acquires.map((acquire, index) => {
      return <AcquireEntry key={index} fields={acquire.fields} />
    });
    const addAnother = <a onClick={this.addAnother}>+ Add another</a>;
    const emptyMessage = <p>No acquire program selected</p>;

    return (
      <div className="acquire-form">
        <h4>Acquires</h4>
        { acquireEntries }
        { this.props.acquires.length ? addAnother : emptyMessage }
      </div>
    );
  }
}

export default AcquireForm;
