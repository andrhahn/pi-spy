import * as mongoose from 'mongoose';

const DeviceSchema = new mongoose.Schema({
  hostName: {
    type: String,
    required: true
  }
});

export = mongoose.model('Device', DeviceSchema);
