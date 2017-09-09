import * as mongoose from 'mongoose';

const DeviceSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  hostName: {
    type: String,
    required: true
  },
  ipAddress: {
    type: String,
    required: true
  }
});

export = mongoose.model('Device', DeviceSchema);
