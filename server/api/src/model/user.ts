import * as mongoose from 'mongoose';

const UserSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true
  }
});

export = mongoose.model('User', UserSchema);
